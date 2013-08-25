"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test forum".
"""

from django.test import TestCase
from django.db import IntegrityError
from forum.models import Post

class PostTestCase(TestCase):
    def setUp(self):
        Post.objects.create(title="cold_joke", content="haha", tags=['cold'])

    def test_get_post_content(self):
        """test get post content"""
        coldJoke = Post.objects.get(title="cold_joke")
        self.assertEqual(coldJoke.tags, ['cold'])

    def test_post_duplicate_check(self):
        """test get post content"""
        # create duplicate one
        self.assertRaises(IntegrityError, Post.objects.create, title="cold_joke", content="haha", \
                          tags=['cold', 'duplicate'])
