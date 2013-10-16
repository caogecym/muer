import urllib2
import httplib
import boto
import logging
from optparse import make_option

from forum.models import Post
from django.core.management.base import BaseCommand

logger = logging.getLogger('muer')
ad_list = ['diogio9888',]

def absolute_delete(post):
    # delete post seed in s3
    s3 = boto.connect_s3()
    bucket = s3.get_bucket('muer')
    for res in post.resources.all():
        logger.info('post %s has res %s, delete...' % (post.id, res.resource_src))
        key = res.resource_src
        # no matter key exist or not
        bucket.delete_key(key)

    # delete post in database
    post.delete()
    logger.info('post has been deleted')

def delete_non_popular_post(post):
    logger.info('deleting post %s with like_count less than 30...' % post.id)
    if post.like_count < 30:
        # delete post and its s3
        absolute_delete(post)

def delete_bad_download_post(post):
    # delete bad download post
    if post.resources.all():
        resource = post.resources.all()[0]
        res_url = resource.resource_src
        if 'rmdown' in res_url:
            logger.info('found bad res_url: %s' % res_url)
            resource.resource_src = ''
            resource.save()
            logger.info('res_url after correct: %s' % resource.resource_src)
        if res_url == '':
            post.delete()
            logger.info('post has been deleted')

def sanitizePostImg(post):
    logger.info('sanitizing post(id = %s) img' % post.id)
    for img in post.images.all():
        # remove empty src
        if img.image_src is None or img.image_src == '':
            logger.info('post(id = %s) has empty img src, deleting...' % post.id)
            img.delete()
            continue

        # remove ads
        for ad_key in ad_list:
            if ad_key in img.image_src:
                logger.info('post(id = %s) has ad diogio9888, deleting...' % post.id)
                img.delete()
                continue
        # invalid src
        try:
            urllib2.urlopen(img.image_src, timeout=5)
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

class Command(BaseCommand):
    help = 'Fix invalid download links'

    option_list = BaseCommand.option_list + (
        make_option('--delete_non_popular',
            action='store_true',
            default=False,
            help='delete not popular posts',
        ),
        make_option('--delete_bad_download',
            action='store_true',
            default=False,
            help='delete posts with bad download links',
        ),
        make_option('--sanitize_img',
            action='store_true',
            default=False,
            help='remove bad imgs, including ad imgs',
        ),
    )

    def handle(self, *args, **options):
        for post in Post.objects.all():
            # delete post count less than threshold
            if options['delete_non_popular']:
                delete_non_popular_post(post)
            if options['delete_bad_download']:
                delete_bad_download_post(post)
            if options['sanitize_img']:
                sanitizePostImg(post)
