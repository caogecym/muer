from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from forum.models import Post
import requests
import lxml
from lxml import html
import time, datetime

class Command(BaseCommand):
    help = 'Scrapes the sites for new dockets'


    def handle(self, *args, **options):
        admin = User.objects.all().filter(username='caogecym')[0]
        self.stdout.write('\nScraping started at %s\n' % str(datetime.datetime.now()))

        sites = {'qiushibaike': 'http://www.qiushibaike.com'}

        for site, url in sites.iteritems():
            self.stdout.write('Scraping url: %s\n' % url)
            r = requests.get(url)
            root = lxml.html.fromstring(r.content)
            # Find the correct table element
            for joke in root.cssselect('div[class="block untagged mb15 bs2"]'):
                joke_title = joke.cssselect('div[class="detail"] a')[0].text_content().strip()
                joke_content = joke.cssselect('div[class="content"]')[0].text_content().strip()
                joke_upvote= joke.cssselect('div[class=bar] ul')[0].text_content().strip().split()[0]

                # create joke object
                if joke_upvote > 500:
                    jokeObject = Post(title=joke_title, content=joke_content, author=admin)
                    jokeObject.save()
