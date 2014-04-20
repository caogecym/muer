"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test forum".
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from forum.models import Post, Tag, Comment, Image, Resource
import logging
logger = logging.getLogger(__name__)


class ClientTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='caogecym', password='42')
        user_1 = User.objects.create_user(username='ycao', password='42')
        user.save()
        user_1.save()
        Post.objects.create(title="test_post", content="Ultimate anwser to everything: 42", author=user)

    def test_login(self):
        c = Client()
        res = c.login(username='caogecym', password='42')
        self.assertTrue(res)

    def test_register(self):
        pass

    def test_new_post_success(self):
        c = Client()
        c.login(username='caogecym', password='42')
        c.post('/posts/new_post/', {'title':'new post', 'content':'new content', 'tagnames':'cold-joke animal'})
        self.assertEqual(len(Post.objects.filter(title='new post')), 1)
        
    def test_new_post_login_required(self):
        c = Client()
        c.post('/posts/new_post/', {'title':'new post', 'content':'new content', 'tagnames':'cold-joke animal'})
        self.assertEqual(len(Post.objects.filter(title='new post')), 0)

    def test_update_post(self):
        c = Client()
        c.login(username='caogecym', password='42')
        post = Post.objects.filter(title="test_post")[0]
        res = c.post('/posts/{}/edit/'.format(post.id), {'title':post.title, 'content':'updated content', 
                     'tagnames':'needs-to-be-fixed'})
        self.assertEqual(Post.objects.filter(title='test_post')[0].content, '<p>updated content</p>')

    def test_update_post_owner_only(self):
        ''' update forbidden by different user '''
        c = Client()
        c.login(username='ycao', password='42')
        post = Post.objects.filter(title="test_post")[0]
        res = c.post('/posts/{}/edit/'.format(post.id), {'title':post.title, 'content':'updated content', 
                     'tagnames':'needs-to-be-fixed'})
        self.assertEqual(res.status_code, 403)

    def test_delete_post(self):
        c = Client()
        c.login(username='caogecym', password='42')
        post = Post.objects.filter(title="test_post")[0]
        c.post('/posts/{}/delete/'.format(post.id))
        self.assertTrue(Post.objects.filter(title='test_post')[0].deleted)

    def test_delete_post_owner_only(self):
        c = Client()
        c.login(username='ycao', password='42')
        post = Post.objects.filter(title="test_post")[0]
        c.post('/posts/{}/delete/'.format(post.id))
        self.assertFalse(Post.objects.filter(title='test_post')[0].deleted)

    def test_like_post(self):
        pass

    def test_unlike_post(self):
        pass
