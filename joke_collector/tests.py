"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test joke_collector".
"""

from django.test import TestCase
from joke_collector.models import Joke

class JokeTestCase(TestCase):
    def setUp(self):
        Joke.objects.create(title="cold_joke", content="haha", tags=['cold'])

    def test_get_joke_content(self):
        """test get joke content"""
        coldJoke = Joke.objects.get(title="cold_joke")
        self.assertEqual(coldJoke.tags, ['cold'])
