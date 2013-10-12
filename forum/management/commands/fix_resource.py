from forum.models import Post
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Scrapes the sites for new threads'
    def handle(self, *args, **options):
        for post in Post.objects.all():
            if post.resources.all():
                resource = post.resources.all()[0]
                res_url = resource.remote_resource_src
                if 'rmdown' in res_url:
                    self.stdout.write('found bad res_url: %s' % res_url)
                    resource.remote_resource_src = ''
                    resource.save()
                    self.stdout.write('res_url after correct: %s' % resource.remote_resource_src)
