import urllib2
import boto
import logging

from forum.models import Post
from django.core.management.base import BaseCommand

ad_list = []
logger = logging.getLogger('muer')

class Command(BaseCommand):
    help = 'Scrapes the sites for new threads'
    def handle(self, *args, **options):
        for post in Post.objects.all():
            # remove bad download
            if post.resources.all():
                resource = post.resources.all()[0]
                res_url = resource.remote_resource_src
                if 'rmdown' in res_url:
                    logger.info('found bad res_url: %s' % res_url)
                    resource.remote_resource_src = ''
                    resource.save()
                    logger.info('res_url after correct: %s' % resource.remote_resource_src)

            # fix bad download for rmdown case

            # remove empty and invalid src
            self.sanitizeImg(post)

            # remove post without any src
            if not post.images.all():
                logger.info('post %s has empty img src, delete...' % post.id)
                # delete post seed in s3
                s3 = boto.connect_s3()
                bucket = s3.get_bucket('muer')
                for res in post.resources.all():
                    logger.info('post %s has res %s, delete...' % (post.id, res.remote_resource_src))
                    key = res.remote_resource_src
                    # no matter key exist or not
                    bucket.delete_key(key)

                # delete post in database
                post.delete()
                logger.info('post has been deleted')

    def sanitizeImg(self, post):
        logger.info('sanitizing post(id = %s) img' % post.id)
        for img in  post.images.all():
            # empty src
            if img.remote_image_src is None or img.remote_image_src == '':
                img.delete()
                return
            # invalid src
            try:
                urllib2.urlopen(img.remote_image_src, timeout=5)
            except urllib2.URLError:
                logger.info('img connection error, delete this img')
                img.delete()
            except UnicodeEncodeError:
                logger.info('img url not standard, delete this img')
                img.delete()

            # remove ads


