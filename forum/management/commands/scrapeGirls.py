# coding=utf8
import os
import re
import uuid
import logging

import boto
from optparse import make_option

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files import File
from django.db import IntegrityError, transaction
from forum.models import Post, Image, Resource, Tag
from forum.management.commands.fix_images import ad_list

from django.conf import settings
import requests
import urllib2, urllib
import lxml
from lxml import html
from lxml.etree import fromstring, tostring
from bs4 import BeautifulSoup
from datetime import datetime

def enum(**enums):
    return type('Enum', (), enums)

SiteType = enum(RMDOWN=1, VII=2)
BASE_URL = 'http://184.154.128.243/'
MIN_SEED_SIZE = 10000
logger = logging.getLogger('muer')

class Command(BaseCommand):
    help = 'Scrapes the sites for new threads'
    try:
        user = User.objects.all()[0]
    except IndexError:
        logger.error('no user found')
            
    option_list = BaseCommand.option_list + (
        make_option('--debug',
            action='store_true',
            default=False,
            help='Enter debug mode'),
        make_option('--noupload',
            action='store_true',
            default=False,
            help='No seed to be uploaded'),
        )

    def handle(self, *args, **options):
        logger.info('\nScraping started at %s\n' % str(datetime.now()))
        sub_sites = {
                     'caoliu-asia-no-mosaic': 'http://184.154.128.243/thread0806.php?fid=2',
                     'caoliu-asia-with-mosaic': 'http://184.154.128.243/thread0806.php?fid=15',
                     'caoliu-eu': 'http://184.154.128.243/thread0806.php?fid=4',
                     'caoliu-cartoon': 'http://184.154.128.243/thread0806.php?fid=5',
                    }

        self.initTags()

        # get thread addressses
        if options['debug']:
            thread_addresses = [('no-mosaic', args[0])]
        else:
            thread_addresses = []
            for site_type, list_url in sub_sites.iteritems():
                # get page info
                try:
                    r = requests.get(list_url)
                except requests.ConnectionError, e:
                    logger.error('ERROR: %s' % e.message)
                    continue
                p = re.compile(r'<head.*?/head>', flags=re.DOTALL)
                content = p.sub('', r.content)
                soup = BeautifulSoup(content, from_encoding="gb18030")
                page_div = soup.find("div", { "class" : "pages" }).text
                page_count = int(page_div.partition('/')[-1].rpartition('total')[0].strip())
                page = 1
                for i in range(int(page_count/10)):
                    thread_url = list_url + '&search=&page=' + str(page)

                    # set threshold if givin in args
                    threshold = int(args[0]) if len(args) > 0 else 30

                    if thread_addresses == None:
                        thread_addresses = self.getThreadsFrom(site_type, thread_url, threshold=threshold)
                    else:
                        thread_addresses.extend(self.getThreadsFrom(site_type, thread_url, threshold=threshold))
                    page += 1

        for thread_type, thread_sub_url, like_count in thread_addresses:
            self.createPost(BASE_URL+thread_sub_url, Command.user, thread_type, like_count, *args, **options)

    def getThreadsFrom(self, site_type, url, threshold):
        thread_addresses = []
        logger.info('Filtering threads in url: %s\n' % url)

        try:
            r = requests.get(url)
        except requests.ConnectionError, e:
            logger.error('ERROR: %s' % e.message)
            return []

        p = re.compile(r'<head.*?/head>', flags=re.DOTALL)
        content = p.sub('', r.content)
        soup = BeautifulSoup(content, from_encoding="gb18030")

        # get filtered post address
        for thread in soup.findAll("tr", { "class" : "tr3 t_one" }):
            try:
                # filter by reply number and getting rid of topped topics
                thread_time = thread.find("div", { "class" : "f10" }).text 
                thread_year = datetime.strptime(thread_time, '%Y-%m-%d').year
                thread_reply_count = int(thread.find("td", { "class" : "tal f10 y-style" }).text.strip())
                if thread_reply_count > threshold and datetime.now().year - thread_year < 1:
                    thread_addresses.append((site_type, thread.h3.a['href'], thread_reply_count))
                else:
                    logger.info('skip thread: %s, reply_count: %s, create_date: %s\n' 
                            % (thread.h3.a['href'], thread_reply_count, thread_time))
            except:
                logger.error('Get thread address failed, time: %s, reply: %s\n' % (thread_time, thread_reply_count))
                continue
        return thread_addresses
    
    def initTags(self):
        user = Command.user
        try:
            self.tag_asia = Tag.objects.get(name='asia')
        except:
            self.tag_asia = Tag(name='asia', author=user)
            self.tag_asia.save()

        try:
            self.tag_no_mosaic = Tag.objects.get(name='no-mosaic')
        except:
            self.tag_no_mosaic = Tag(name='no-mosaic', author=user)
            self.tag_no_mosaic.save()

        try:
            self.tag_with_mosaic = Tag.objects.get(name='with-mosaic')
        except:
            self.tag_with_mosaic = Tag(name='with-mosaic', author=user)
            self.tag_with_mosaic.save()

        try:
            self.tag_eu = Tag.objects.get(name='europe')
        except:
            self.tag_eu = Tag(name='europe', author=user)
            self.tag_eu.save()

        try:
            self.tag_cartoon = Tag.objects.get(name='cartoon')
        except:
            self.tag_cartoon = Tag(name='cartoon', author=user)
            self.tag_cartoon.save()

    def createPost(self, thread_url, user, thread_type=None, like_count=0, *args, **options):
        url = thread_url
        logger.info('getting filtered thread content in url: %s\n' % url)
        
        try:
            r = requests.get(url)
        except requests.ConnectionError, e:
            logger.error('ERROR: %s' % e.message)
            return
        p = re.compile(r'<head.*?/head>', flags=re.DOTALL)
        content = p.sub('', r.content)
        # solve &lt;&gt; problem
        soup = BeautifulSoup(content, from_encoding="gb18030")
        new_soup = soup.prettify(formatter=None)
        soup = BeautifulSoup(new_soup, from_encoding="gb18030")

        thread_title = soup.h4.text
        thread_content = soup.find('div', {'class':'tpc_content'})

        try: 
            post = Post(title=thread_title, content='', author=user, post_source_name='草榴社区', 
                        post_source_url=url, like_count = like_count)
            post.save()
            self.createTagsForPost(post.id, url, thread_type)
            logger.info('post %s created successfully \n' % post.id)
        except IntegrityError, e:
            post = Post.objects.get(title=thread_title)
            if post:
                logger.info('post existed, but will update like count')
                post.like_count = like_count
            logger.error('ERROR: %s' % e.message)

        else:
            # load images
            thread_imgs = soup.findAll('img', {"style":"cursor:pointer"})
            for img in thread_imgs:
                for key in ad_list:
                    if key in img['src']:
                        continue
                if img['src']:
                    image = Image(content_object=post, image_src=img['src'])
                    image.save()
            logger.info('post %s images recorded successfully \n' % post.id)

            # delete post without any images
            if not post.images.all():
                post.delete()
                logger.info('post %s has empty image, deleted \n' % post.id)
                return

            seed_src = self.getResource(post.id, thread_title, thread_content, *args, **options)

            # delete post without seed
            if not seed_src:
                logger.warning('no seed found for post %s' % post.id)
                post.delete()
                return
            thread_resource = Resource(content_object=post, resource_src=seed_src)
            thread_resource.save()
            logger.info('parsed seed %s for post: %s successfully' % (thread_resource.resource_src, post.id))

    def createTagsForPost(self, post_id, url, thread_type):
        logger.info('creating post %s tag\n' % post_id)
        post = Post.objects.get(id=post_id)
        if 'no-mosaic' in thread_type:
            post.tags.add(self.tag_asia, self.tag_no_mosaic)
        elif 'with-mosaic' in thread_type:
            post.tags.add(self.tag_asia, self.tag_with_mosaic)
        elif 'eu' in thread_type:
            post.tags.add(self.tag_eu)
        elif 'cartoon' in thread_type:
            post.tags.add(self.tag_cartoon)

    def getResource(self, post_id, thread_title, thread_content, *args, **options):
        # rmdown
        soup = thread_content
        pattern = re.compile(r'rmdown')
        src = soup.find(text=pattern)
        if src is not None:
            r_src = self.create_torrent(post_id, SiteType.RMDOWN, src.strip(), thread_title, *args, **options)
            return r_src

        # Seed Torrent
        pattern = re.compile(r'seed')
        txt = soup.find(text=pattern)
        if txt is not None:
            return txt.findNext('a')['href']

        # xiazaidizhi
        pattern = re.compile(ur'[\u4e0b\u8f7d\u5730\u5740]+', re.UNICODE)
        txt = soup.find(text=pattern)
        if txt is not None:
            return txt.findNext('a')['href']
        else:
            return ''

    def create_torrent(self, post_id, site, url, title, *args, **options):
        if site == SiteType.RMDOWN:
            try:
                r = requests.get(url)
            except requests.ConnectionError, e:
                logger.error('ERROR: %s' % e.message)
                return ''
            soup = BeautifulSoup(r.content, from_encoding="utf-8")
            ref = soup.findAll('input')[0]['value']
            reff = soup.findAll('input')[1]['value']
            form_data = [('ref', ref),
                         ('reff', reff),
                        ]
            form_data = urllib.urlencode(form_data)

            path = 'http://www.rmdown.com/download.php'
            req = urllib2.Request(path, form_data)
            req.add_header("Content-type", "application/x-www-form-urlencoded")

            seed_name = ref + '.torrent'
            seed_url = 'seeds/' + seed_name
            try:
                torrent = urllib2.urlopen(req)
            except Exception, e:
                logger.error('unexpected error happened when getting seed for post: %s, %s' % (post_id, e))
                return ''

            if options['debug'] or options['noupload']:
                pass
            else:
                self.upload_to_s3(post_id, torrent, seed_name)
            return seed_url

    def upload_to_s3(self, post_id, f, name):
        logger.info('post %s seed %s uploading\n' % (post_id, name))
        s3 = boto.connect_s3()
        bucket = s3.get_bucket('muer')
        key = s3.get_bucket('muer').new_key('seeds/%s' % name)
        key.set_contents_from_string(f.read())
        key.set_acl('public-read')
        logger.info('post %s seed %s uploaded\n' % (post_id, name))
