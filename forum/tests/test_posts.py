from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test.client import Client

from rest_framework import status
from rest_framework.test import APITestCase

from forum.models import Post

class PostTests(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='caogecym', password='42')
        self.post = Post.objects.create(title="test_post", content="Ultimate anwser to everything: 42", author=user)

    def test_like_post(self):
        """
        Anybody can like a post.
        """
        self.assertEqual(self.post.like_count, 0)
        url = '/api/posts/1/like/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'status': 'post liked'})
        self.assertEqual(Post.objects.all()[0].like_count, 1)

    def test_unlike_needs_login(self):
        """
        Only logged in user can unlike a post.
        """
        self.assertEqual(self.post.like_count, 0)
        url = '/api/posts/1/unlike/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'status': 'have to login to unlike'})
        self.assertEqual(Post.objects.all()[0].like_count, 0)

    def test_logged_in_can_unlike(self):
        c = Client()
        res = c.login(username='caogecym', password='42')

        self.assertEqual(self.post.like_count, 0)
        url = '/api/posts/1/unlike/'
        response = c.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'status': 'post unliked'})
        self.assertEqual(Post.objects.all()[0].like_count, -1)
