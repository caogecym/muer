import os
import re

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files import File
from django.db import IntegrityError
from forum.models import Post, Image, Resource

import settings
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
MIN_SEED_SIZE = 10000

class Command(BaseCommand):
    help = 'Scrapes the sites for new threads'

    def handle(self, *args, **options):
        try:
            admin = User.objects.all()[0]
        except IndexError:
            self.stdout.write('no user found')
            
        self.stdout.write('\nScraping started at %s\n' % str(datetime.now()))
        BASE_URL = 'http://184.154.128.243/'
        sites = {'caoliu-asia': 'http://184.154.128.243/thread0806.php?fid=2',
                 #'asia-page2': 'http://184.154.128.243/thread0806.php?fid=2&search=&page=2'
                }
        thread_addresses = []

        # filtering threads
        for site, url in sites.iteritems():
            self.stdout.write('Filtering threads in url: %s\n' % url)

            r = requests.get(url)
            p = re.compile(r'<head.*?/head>', flags=re.DOTALL)
            content = p.sub('', r.content)
            soup = BeautifulSoup(content, from_encoding="gb18030")

            # get filtered post address
            for thread in soup.findAll("tr", { "class" : "tr3 t_one" }):
                # filter by reply number and getting rid of topped topics
                thread_time = thread.find("div", { "class" : "f10" }).text 
                thread_year = datetime.strptime(thread_time, '%Y-%m-%d').year
                thread_reply_count = thread.find("td", { "class" : "tal f10 y-style" }).text
                if  thread_reply_count > 30 and datetime.now().year - thread_year < 1:
                    thread_addresses.append(thread.h3.a['href'])

        # get title, content for filtered posts
        for sub_url in thread_addresses:
            url = BASE_URL + sub_url
            self.stdout.write('getting filtered thread content in url: %s\n' % url)
            
            r = requests.get(url)
            p = re.compile(r'<head.*?/head>', flags=re.DOTALL)
            content = p.sub('', r.content)
            # solve &lt;&gt; problem
            soup = BeautifulSoup(content, from_encoding="gb18030")
            new_soup = soup.prettify(formatter=None)
            soup = BeautifulSoup(new_soup, from_encoding="gb18030")

            thread_title = soup.h4.text
            thread_content = soup.find('div', {'class':'tpc_content'})


            try: 
                post = Post(title=thread_title, content=thread_content, author=admin)
                post.save()
                self.stdout.write('post %s created successfully \n' % thread_title)
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
                self.stdout.write('post %s images recorded successfully \n' % thread_title)

                (r_src, l_src) = self.getResource(thread_content)
                thread_resource = Resource(content_object=post, remote_resource_src=r_src, local_resource_src=l_src)
                self.stdout.write('parsed seed %s for post: %s successfully' % (thread_resource.remote_resource_src, post.title))
                thread_resource.save()

    def getResource(self, thread_content):
        # rmdown
        soup = thread_content
        pattern = re.compile(r'rmdown')
        src = soup.find(text=pattern)
        if src is not None:
            r_src = src.strip()
            l_src = self.create_torrent(site=SiteType.RMDOWN, url=r_src)
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

    def create_torrent(self, site, url):
        if site == SiteType.RMDOWN:
            r = requests.get(url)
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
            seed_path = settings.FORUM_ROOT + '/static/seeds/'
            seed_url = seed_path + seed_name
            torrent = urllib2.urlopen(req)
            with open(seed_url, 'w') as f:
                seed = File(f)
                seed.write(torrent.read())
                # invalid seed, remove
                if os.stat(seed_url).st_size < MIN_SEED_SIZE:
                    self.stdout.write('post %s seed download failed\n' % thread_title)
                    os.remove(seed_url)
                    return ''
            return 'seeds/' + seed_name
