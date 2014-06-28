import os
import sys
import getopt
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
from forum.management.commands.fix_resource import ad_list

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
                     'month-best': 'http://www.qiushibaike.com/month/',
                    }

        self.initTags()

        # get thread addressses
        if options['debug']:
            thread_addresses = [('no-mosaic', args[0])]
        else:
            for site_type, list_url in sub_sites.iteritems():
                # get page info
                try:
                    r = requests.get(list_url)
                except requests.ConnectionError, e:
                    logger.error('ERROR: %s' % e.message)
                    continue

                page_count = options['page_count']
                page = 1
                for i in range(page_count):
                    page_url = list_url + 'page/' + str(page)

                    # set threshold if givin in args
                    quality_ratio = int(args[0]) if len(args) > 0 else 20

                    self.createJokes(page_url, Command.user, quality_ratio, *args, **options)
                    page += 1

    def createJokes(self, url, user, quality_ratio, *args, **options):
        logger.info('Creating jokes in url: %s\n' % url)

        try:
            r = requests.get(url, timeout=30)
        except requests.ConnectionError, e:
            logger.error('ERROR: %s' % e.message)
            return []

        p = re.compile(r'<head.*?/head>', flags=re.DOTALL)
        content = p.sub('', r.content)
        soup = BeautifulSoup(content, from_encoding="utf-8")

        # get filtered post address
        for joke in soup.findAll("div", { "class" : "block untagged mb15 bs2" }):
            try:
                like_count = int(joke.find('li', {"class" : "up"}).a.text)
                dislike_count = abs(int(joke.find('li', {"class" : "down"}).a.text))
                joke_id = joke['id'].split('_')[-1]

                # filter by quality_ratio=like/dislike
                if float(like_count/dislike_count) < quality_ratio:
                    logger.info('skip joke: %s, like_count: %s, dislike_count: %s\n' 
                            % (joke_id, like_count, dislike_count))
                    continue

                joke_content = joke.find('div', {'class':'content'}).text
                joke_time = joke.find('div', {'class':'content'})['title']
                joke_url = 'www.qiushibaike.com/article/' + str(joke_id)

                post = Post(title=joke_content[:10], content=joke_content, author=user, post_source_name='糗事百科', 
                            post_source_url=joke_url, like_count=like_count)
                post.save()
                post.tags.add(self.tag_qiubai)

                logger.info('post %s created successfully \n' % joke_id)

            except IntegrityError, e:
                #post = Post.objects.get(post_source_url=joke_url)
                #if post:
                    #logger.info('post existed, but will update like count')
                    #post.like_count = like_count
                logger.error('ERROR: Create joke %s failed, %s' % (joke_id, e.message))

            except Exception, e:
                logger.error('Create joke failed: %s, %s\n' % (joke_id, e))

            else:
                # load images
                joke_img_divs = joke.findAll('div', {"class":"thumb"})
                for img_div in joke_img_divs:
                    if img_div.img['src']:
                        image = Image(content_object=post, image_src=img_div.img['src'])
                        image.save()
                logger.info('joke %s images recorded successfully \n' % joke_id)

    def initTags(self):
        user = Command.user
        try:
            self.tag_qiubai = Tag.objects.get(name='糗事百科')
        except:
            self.tag_qiubai = Tag(name='糗事百科', author=user)
            self.tag_qiubai.save()
