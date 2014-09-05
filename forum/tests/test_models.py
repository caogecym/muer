"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test forum".
"""

from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User
from forum.models import Post, Tag, Comment, Image, Resource
import logging
logger = logging.getLogger(__name__)


class PostTestCase(TestCase):
    def setUp(self):
        logger.info('Initializing post test...')
        user = User(username='caogecym')
        user1 = User(username='caogecym1')
        user2 = User(username='caogecym2')
        user.save()
        user1.save()
        user2.save()
        Post.objects.create(title="test_post", content="Ultimate anwser to everything: 42", author=user)

    def test_tag(self):
        logger.info('start testing test_tag...')
        post = Post.objects.get(title='test_post')
        user = post.author
        # tag1 no author
        tag1 = Tag(name='cold')
        tag1.save()
        # tag2 with author
        tag2 = Tag(name='science', author=user)
        tag2.save()
        post.tags.add(tag1)
        post.tags.add(tag2)
        self.assertEqual(len(post.tags.all()), 2)

    def test_image(self):
        logger.info('start testing test_image...')
        post = Post.objects.get(title='test_post')
        # tag1 no author
        image1 = Image(content_object=post, image_src='www.caogecym.com/img1.jpg')
        image1.save()
        # tag2 with author
        image2 = Image(content_object=post, image_src='www.caogecym.com/img2.jpg')
        image2.save()
        self.assertEqual(len(post.images.all()), 2)

    def test_resource(self):
        logger.info('start testing test_resource...')
        post = Post.objects.get(title='test_post')
        resource1 = Resource(content_object=post, resource_src='www.caogecym.com/img1.torrent')
        resource1.save()
        resource2 = Resource(content_object=post, resource_src='www.caogecym.com/img2.torrent')
        resource2.save()
        self.assertEqual(len(post.resources.all()), 2)

    def test_liked_by(self):
        logger.info('start testing test_liked_by...')
        post = Post.objects.get(title='test_post')
        user1 = User.objects.all().filter(username='caogecym1')[0]
        user2 = User.objects.all().filter(username='caogecym2')[0]
        post.liked_by.add(user1)
        post.liked_by.add(user2)
        self.assertEqual(len(post.liked_by.all()), 2)

    def test_post_duplicate_check(self):
        logger.info('start testing test_post_duplicate_check...')
        """test get post content"""
        # create duplicate one
        user = User.objects.filter(username='caogecym')[0]
        self.assertRaises(IntegrityError, Post.objects.create, title="test_post", content="haha", author=user)
