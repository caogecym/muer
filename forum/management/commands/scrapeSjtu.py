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
from django.db import IntegrityError, DatabaseError, transaction
from forum.models import Post, Image, Resource, Tag
from forum.management.commands.fix_resource import ad_list
from utils.string_utils import find_between

from django.conf import settings
import requests
import urllib2, urllib
import lxml
from lxml import html
from lxml.etree import fromstring, tostring
from bs4 import BeautifulSoup
from datetime import datetime

BASE_URL = 'http://bbs.sjtu.edu.cn/'
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
        make_option('-p', '--page',
            action='store',
            type='int',
            default=1,
            dest='page_count',
            help='number of page to parse',)
        )

    def handle(self, *args, **options):
        logger.info('\nScraping started at %s\n' % str(datetime.now()))
        sub_sites = {
                      'sjtu-joke': 'http://bbs.sjtu.edu.cn/bbstdoc,board,joke.html',
                    }

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
                page_count = options['page_count']
                for i in range(page_count):
                    thread_url = 'http://bbs.sjtu.edu.cn/bbstdoc,board,joke,page,' + str(i) + '.html'

                    # set threshold if givin in args
                    threshold = int(args[0]) if len(args) > 0 else 0

                    if thread_addresses == None:
                        thread_addresses = self.getThreadsFrom(site_type, thread_url, threshold=threshold)
                    else:
                        thread_addresses.extend(self.getThreadsFrom(site_type, thread_url, threshold=threshold))

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

        # get filtered post address, start with '○ '
        for thread in soup.findAll('a', text=re.compile(u'[\u25cb]')):
            try:
                # filter by reply number and getting rid of topped topics
                st = thread.nextSibling
                thread_reply_count = int(re.findall('\d+', st)[0])
                if thread_reply_count >= threshold: 
                    thread_addresses.append((site_type, thread['href'], thread_reply_count))
                else:
                    logger.info('skip thread: %s, reply_count: %s\n' 
                            % (thread['href'], thread_reply_count))
            except:
                logger.error('Get thread address failed, reply: %s\n' % (thread_reply_count))
                continue
        return thread_addresses
    
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

        body = soup.pre
        # extract title
        start = u'\n\u6807  \u9898: '
        end = u'\n'
        thread_title = find_between(body.text, start, end)

        # split header and content and signature
        start = u'\n\u53d1\u4fe1\u7ad9: '
        end = u'\n'
        thread_header_spliter = find_between(body.text, start, end, inclusive=True)

        thread_content = body.text.split(thread_header_spliter)[-1].split(u'\n--\n')[0]

        try: 
            post = Post(title=thread_title, content=thread_content, author=user, post_source_name='饮水思源', 
                        post_source_url=url, like_count=like_count)
            post.save()
            logger.info('post %s created successfully \n' % post.id)
        except IntegrityError, e:
            post = Post.objects.get(title=thread_title)
            if post:
                logger.error('post existed, but will update like count')
                post.like_count = like_count
            logger.error('ERROR: %s' % e.message)
        except DatabaseError, e:
            logger.error('ERROR: %s' % e.message)
        except Exception, e:
            logger.error('ERROR: %s' % e.message)

        else:
            # load images
            thread_imgs = body.findAll('img')
            for img in thread_imgs:
                for key in ad_list:
                    if key in img['src']:
                        continue
                if img['src']:
                    image = Image(content_object=post, image_src=img['src'])
                    image.save()
            logger.info('post %s images recorded successfully \n' % post.id)

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

