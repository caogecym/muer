from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test.client import Client

from rest_framework import status
from rest_framework.test import APITestCase

from forum.models import Post, Tag

class PostTests(APITestCase):
    def setUp(self):
        normal_user_0 = User.objects.create_user(username='caogecym', password='42')
        normal_user_1 = User.objects.create_user(username='caogecym1', password='421')
        super_user = User.objects.create_user(username='admin', password='adminpw')
        super_user.is_staff = True
        super_user.save()

        self.post = Post.objects.create(title="test_post", content="Ultimate anwser to everything: 42",
        author=normal_user_0)
        self.post1 = Post.objects.create(title="test_post_1", content="Ultimate anwser to everything: 42",
        author=normal_user_1)
        Tag.objects.create(name="animal", author=normal_user_0)
        print "In method %s" % self._testMethodName

    def test_like_post(self):
        """
        Anybody can like a post.
        """
        self.assertEqual(self.post.like_count, 0)
        url = '/api/posts/1/like'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'status': 'post liked'})
        self.assertEqual(Post.objects.all()[0].like_count, 1)

    def test_unlike_needs_login(self):
        """
        Only logged in user can unlike a post.
        """
        self.assertEqual(self.post.like_count, 0)
        url = '/api/posts/1/unlike'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {'status': 'have to login to unlike'})
        self.assertEqual(Post.objects.all()[0].like_count, 0)

    def test_logged_in_can_unlike(self):
        res = self.client.login(username='caogecym', password='42')
        self.assertEqual(self.post.like_count, 0)
        url = '/api/posts/1/unlike'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'status': 'post unliked'})
        self.assertEqual(Post.objects.all()[0].like_count, -1)

    def test_unlogged_in_get_list(self):
        url = '/api/posts'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unlogged_in_get_detail(self):
        url = '/api/posts/1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unlogged_in_post(self):
        url = '/api/posts'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unlogged_in_put(self):
        url = '/api/posts/1'
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unlogged_in_delete(self):
        url = '/api/posts/1'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_normal_user_get_list(self):
        url = '/api/posts'
        res = self.client.login(username='caogecym', password='42')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_normal_user_get_detail(self):
        url = '/api/posts/1'
        res = self.client.login(username='caogecym', password='42')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_normal_user_post(self):
        url = '/api/posts'
        res = self.client.login(username='caogecym', password='42')
        data = {'title':'new post', 'content':'new content', 'author':1, 'tags':[1]}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_normal_user_put_self(self):
        url = '/api/posts/1'
        res = self.client.login(username='caogecym', password='42')
        data = {'title':'updated post', 'content':'new content', 'author':1, 'tags':[1]}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_normal_user_put_other(self):
        url = '/api/posts/2'
        res = self.client.login(username='caogecym', password='42')
        data = {'title':'updated post', 'content':'new content', 'author':1, 'tags':[1]}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_normal_user_delete_self(self):
        url = '/api/posts/1'
        res = self.client.login(username='caogecym', password='42')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_normal_user_delete_other(self):
        url = '/api/posts/2'
        res = self.client.login(username='caogecym', password='42')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_get_list(self):
        url = '/api/posts'
        res = self.client.login(username='admin', password='adminpw')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_get_detail(self):
        url = '/api/posts/1'
        res = self.client.login(username='admin', password='adminpw')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_post(self):
        url = '/api/posts'
        res = self.client.login(username='admin', password='adminpw')
        data = {'title':'new post', 'content':'new content', 'author':1, 'tags':[1]}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_put(self):
        url = '/api/posts/1'
        res = self.client.login(username='admin', password='adminpw')
        data = {'title':'updated post', 'content':'new content', 'author':1, 'tags':[1]}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_delete(self):
        url = '/api/posts/1'
        res = self.client.login(username='admin', password='adminpw')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
