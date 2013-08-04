from django.core.management.base import BaseCommand
from htmlParser.models import Joke
import requests
import lxml
from lxml import html
import time, datetime

class Command(BaseCommand):
    help = 'Scrapes the sites for new dockets'

    def handle(self, *args, **options):
        self.stdout.write('\nScraping started at %s\n' % str(datetime.datetime.now()))

        sites = {'qiushibaike': 'http://www.qiushibaike.com'}

        for site, url in sites.iteritems():
            self.stdout.write('Scraping url: %s\n' % url)
            r = requests.get(url)
            root = lxml.html.fromstring(r.content)
            # Find the correct table element
            for joke in root.cssselect('div[class="block untagged mb15 bs2"]'):
                joke_title = joke.cssselect('div[class="detail"] a')[0].text_content().strip()
                joke_content = joke.cssselect('div')[2].text_content().strip()
                #joke_content = joke.cssselect('div[class="content"]')[0].text_content().strip()
                joke_upvote= joke.cssselect('div[class=bar] ul')[0].text_content().strip().split()[0]

                # create joke object
                if joke_upvote > 500:
                    jokeObject = Joke(title=joke_title, content=joke_content, like=joke_upvote)
                    jokeObject.save()
