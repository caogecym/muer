from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from forum.models import Post, Image

import requests
import urllib
import lxml
from lxml import html
from lxml.etree import fromstring, tostring
from bs4 import BeautifulSoup
import re
from datetime import datetime
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Scrapes the sites for new threads'


    def handle(self, *args, **options):
        admin = User.objects.all().filter(username='ycao')[0]
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
            except e:
                self.stdout.write('ERROR: %s' % e.message)

            post.save()
            # load images
            thread_imgs = soup.findAll('img', {"style":"cursor:pointer"})
            for img in thread_imgs:
                # remove thumb imgs
                p = re.compile(r'_thumb', flags=re.DOTALL)
                img_src = p.sub('', img['src'])
                image = Image(content_object=post, remote_image_src=img_src)
                image.save()
