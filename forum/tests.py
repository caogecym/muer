"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test forum".
"""

from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User
from forum.models import Post, Tag, Comment

class PostTestCase(TestCase):
    def setUp(self):
        user = User(username='caogecym')
        user1 = User(username='caogecym1')
        user2 = User(username='caogecym2')
        user.save()
        user1.save()
        user2.save()
        Post.objects.create(title="test_post", content="Ultimate anwser to everything: 42", author=user)

    def test_tag(self):
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

    def test_comment(self):
        post = Post.objects.get(title='test_post')
        user = post.author

        # two comments for post
        comment0 = Comment(content_object=post, author=user, content='I am comment 1')
        comment0.save()
        comment1 = Comment(content_object=post, author=user, content='I am comment 2')
        comment1.save()
        self.assertEqual(len(post.comments.all()), 2)

        # recursive comment for comment0
        comment0_0 = Comment(content_object=comment0, author=user, content='I am comment 0 for comment 1')
        comment0_0.save()
        self.assertEqual(len(post.comments.all().filter(content='I am comment 1')[0].comments.all()), 1)

    def test_liked_by(self):
        post = Post.objects.get(title='test_post')
        user1 = User.objects.all().filter(username='caogecym1')[0]
        user2 = User.objects.all().filter(username='caogecym2')[0]
        post.liked_by.add(user1)
        post.liked_by.add(user2)
        self.assertEqual(len(post.liked_by.all()), 2)
        
    def test_post_duplicate_check(self):
        """test get post content"""
        # create duplicate one
        user = User.objects.filter(username='caogecym')[0]
        self.assertRaises(IntegrityError, Post.objects.create, title="test_post", content="haha", author=user)
