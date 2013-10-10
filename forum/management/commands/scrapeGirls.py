# coding=utf8
import os
import re

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files import File
from django.db import IntegrityError, transaction
from forum.models import Post, Image, Resource, Tag

from django.conf import settings
import requests
import urllib2, urllib
import lxml
from lxml import html
from lxml.etree import fromstring, tostring
from bs4 import BeautifulSoup
from datetime import datetime
import boto
import uuid

def enum(**enums):
    return type('Enum', (), enums)

SiteType = enum(RMDOWN=1, VII=2)
BASE_URL = 'http://184.154.128.243/'
MIN_SEED_SIZE = 10000

class Command(BaseCommand):
    help = 'Scrapes the sites for new threads'

    def handle(self, *args, **options):
        try:
            admin = User.objects.all()[0]
        except IndexError:
            self.stdout.write('no user found')
            
        self.stdout.write('\nScraping started at %s\n' % str(datetime.now()))
        sub_sites = {
                     'caoliu-asia-no-mosaic': 'http://184.154.128.243/thread0806.php?fid=2',
                     'caoliu-asia-with-mosaic': 'http://184.154.128.243/thread0806.php?fid=15',
                     'caoliu-eu': 'http://184.154.128.243/thread0806.php?fid=4',
                     'caoliu-cartoon': 'http://184.154.128.243/thread0806.php?fid=5',
                    }

        self.initTags()

        # get thread addressses
        for site_type, list_url in sub_sites.iteritems():
            # get page info
            try:
                r = requests.get(list_url)
            except requests.ConnectionError, e:
                self.stdout.write('ERROR: %s' % e.message)
                continue

            p = re.compile(r'<head.*?/head>', flags=re.DOTALL)
            content = p.sub('', r.content)
            soup = BeautifulSoup(content, from_encoding="gb18030")
            page_div = soup.find("div", { "class" : "pages" }).text
            page_count = int(page_div.partition('/')[-1].rpartition('total')[0].strip())
            page = 1
            # 10 -> page_count
            for i in range(int(page_count/10)):
                thread_url = list_url + '&search=&page=' + str(page)
                thread_addresses = self.getThreadsFrom(site_type, thread_url)
                page += 1

        for thread_type, thread_sub_url in thread_addresses:
            self.createPost(thread_sub_url, thread_type, admin)

    def initTags(self):
        user = User.objects.all()[0]
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

    def getThreadsFrom(self, site_type, url):
        thread_addresses = []
        self.stdout.write('Filtering threads in url: %s\n' % url)

        try:
            r = requests.get(url)
        except requests.ConnectionError, e:
            self.stdout.write('ERROR: %s' % e.message)
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
                thread_reply_count = thread.find("td", { "class" : "tal f10 y-style" }).text
                if  thread_reply_count > 30 and datetime.now().year - thread_year < 1:
                    thread_addresses.append((site_type, thread.h3.a['href']))
            except:
                self.stdout.write('Get thread address failed, time: %s, reply: %s\n' % (thread_time, thread_reply_count))
                continue
        return thread_addresses
    
    def createPost(self, thread_sub_url, thread_type, admin):
        url = BASE_URL + thread_sub_url
        self.stdout.write('getting filtered thread content in url: %s\n' % url)
        
        try:
            r = requests.get(url)
        except requests.ConnectionError, e:
            self.stdout.write('ERROR: %s' % e.message)
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
            post = Post(title=thread_title, content='', author=admin, post_source_name='草榴社区', post_source_url=url)
            post.save()
            self.createTagsForPost(post.id, url, thread_type)
            self.stdout.write('post %s created successfully \n' % post.id)
        except IntegrityError, e:
            self.stdout.write('ERROR: %s' % e.message)

        else:
            # load images
            thread_imgs = soup.findAll('img', {"style":"cursor:pointer"})
            for img in thread_imgs:
                # remove thumb imgs
                #p = re.compile(r'_thumb', flags=re.DOTALL)
                #img_src = p.sub('', img['src'])
                image = Image(content_object=post, remote_image_src=img['src'])
                image.save()
            self.stdout.write('post %s images recorded successfully \n' % post.id)

            (r_src, l_src) = self.getResource(post.id, thread_title, thread_content)
            thread_resource = Resource(content_object=post, remote_resource_src=r_src, local_resource_src=l_src)
            thread_resource.save()
            self.stdout.write('parsed seed %s for post: %s successfully' % (thread_resource.remote_resource_src, post.id))

    def createTagsForPost(self, post_id, url, thread_type):
        self.stdout.write('creating post %s tag\n' % post_id)
        post = Post.objects.get(id=post_id)
        if 'no-mosaic' in thread_type:
            post.tags.add(self.tag_asia, self.tag_no_mosaic)
        elif 'with-mosaic' in thread_type:
            post.tags.add(self.tag_asia, self.tag_with_mosaic)
        elif 'eu' in thread_type:
            post.tags.add(self.tag_eu)
        elif 'cartoon' in thread_type:
            post.tags.add(self.tag_cartoon)

    def getResource(self, post_id, thread_title, thread_content):
        # rmdown
        soup = thread_content
        pattern = re.compile(r'rmdown')
        src = soup.find(text=pattern)
        if src is not None:
            r_src = src.strip()
            l_src = self.create_torrent(post_id=post_id, site=SiteType.RMDOWN, url=r_src, title=thread_title)
            return (r_src, l_src)

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

    def create_torrent(self, post_id, site, url, title):
        if site == SiteType.RMDOWN:
            try:
                r = requests.get(url)
            except requests.ConnectionError, e:
                self.stdout.write('ERROR: %s' % e.message)
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
            torrent = urllib2.urlopen(req)
            self.upload_to_s3(post_id, torrent, seed_name)
            return seed_url

    def upload_to_s3(self, post_id, f, name):
        self.stdout.write('post %s seed %s uploading\n' % (post_id, name))
        s3 = boto.connect_s3()
        bucket = s3.get_bucket('muer')
        key = s3.get_bucket('muer').new_key('seeds/%s' % name)
        key.set_contents_from_string(f.read())
        key.set_acl('public-read')
        self.stdout.write('post %s seed %s uploaded\n' % (post_id, name))
