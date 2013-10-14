import urllib2
import httplib
import boto
import logging

from forum.models import Post
from django.core.management.base import BaseCommand

ad_list = ['diogio9888',]
logger = logging.getLogger('muer')

class Command(BaseCommand):
    help = 'Scrapes the sites for new threads'
    def handle(self, *args, **options):
        for post in Post.objects.all():
            # set bad download post deleted
            if post.resources.all():
                resource = post.resources.all()[0]
                res_url = resource.remote_resource_src
                if 'rmdown' in res_url:
                    logger.info('found bad res_url: %s' % res_url)
                    resource.remote_resource_src = ''
                    resource.save()
                    logger.info('res_url after correct: %s' % resource.remote_resource_src)
                if res_url == '':
                    post.deleted = True
                    post.save()

            # fix bad download for rmdown case

            # remove empty and invalid src
            self.sanitizePostImg(post)


    def sanitizePostImg(self, post):
        logger.info('sanitizing post(id = %s) img' % post.id)
        for img in post.images.all():
            # remove empty src
            if img.remote_image_src is None or img.remote_image_src == '':
                logger.info('post(id = %s) has empty img src, deleting...' % post.id)
                img.delete()
                continue

            # remove ads
            for ad_key in ad_list:
                if ad_key in img.remote_image_src:
                    logger.info('post(id = %s) has ad diogio9888, deleting...' % post.id)
                    img.delete()
                    continue
            # invalid src
            try:
                urllib2.urlopen(img.remote_image_src, timeout=5)
            except urllib2.URLError:
                logger.info('img connection error, delete this img')
                img.delete()
            except urllib2.URLError, e:
                logger.error('URLError = ' + str(e.reason))
            except httplib.HTTPException, e:
                logger.error('HTTPException')
            except UnicodeEncodeError:
                logger.info('img url not standard, delete this img')
                img.delete()
            except Exception:
                import traceback
                logger.error('generic exception: ' + traceback.format_exc())

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
            post.deleted = True
            post.save()
            logger.info('post has been deleted')

