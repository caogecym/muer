import urllib2
import httplib
import boto
import logging

from forum.models import Post
from django.core.management.base import BaseCommand

logger = logging.getLogger('muer')

class Command(BaseCommand):
    help = 'Fix invalid download links'
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
                    if resource.local_resource_src:
                        resource.remote_resource_src = resource.local_resource_src
                        resource.save()
                        logger.info('post: %s seed url has been updated' % post.id)
                    else:
                        post.delete()
                        logger.info('post has been deleted')

            # fix bad download for rmdown case
