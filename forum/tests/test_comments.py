from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test.client import Client

from rest_framework import status
from rest_framework.test import APITestCase

from forum.models import Post, Tag, Comment

class CommentTests(APITestCase):
    def setUp(self):
        normal_user = User.objects.create_user(username='caogecym', password='42')
        another_user = User.objects.create_user(username='other_user', password='42')
        super_user = User.objects.create_user(username='admin', password='adminpw')
        super_user.is_staff = True
        super_user.save()
        self.post = Post.objects.create(title="test_post", content="Ultimate anwser to everything: 42", 
                                        author=normal_user)
        Comment.objects.create(content='this is hilarious!', post=self.post, author=normal_user)

        print "In method %s" % self._testMethodName

    def test_unlogged_in_get_list(self):
        url = '/api/comments/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unlogged_in_get_detail(self):
        url = '/api/comments/1/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unlogged_in_post(self):
        url = '/api/comments/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unlogged_in_patch(self):
        url = '/api/comments/1/'
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unlogged_in_delete(self):
        url = '/api/comments/1/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_normal_user_get_list(self):
        url = '/api/comments/'
        res = self.client.login(username='caogecym', password='42')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_normal_user_get_detail(self):
        url = '/api/comments/1/'
        res = self.client.login(username='caogecym', password='42')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_normal_user_post(self):
        url = '/api/comments/'
        res = self.client.login(username='caogecym', password='42')
        data = {'content':'new comment', 'post': 1, 'author':1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_normal_user_self_patch(self):
        url = '/api/comments/1/'
        res = self.client.login(username='caogecym', password='42')
        data = {'name':'new_joke', 'author':1}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_normal_user_other_patch(self):
        url = '/api/comments/1/'
        res = self.client.login(username='other_user', password='42')
        data = {'name':'new_joke', 'author':1}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_normal_user_other_delete(self):
        url = '/api/comments/1/'
        res = self.client.login(username='other_user', password='42')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_normal_user_self_delete(self):
        url = '/api/comments/1/'
        res = self.client.login(username='caogecym', password='42')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_get_list(self):
        url = '/api/comments/'
        res = self.client.login(username='admin', password='adminpw')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_get_detail(self):
        url = '/api/comments/1/'
        res = self.client.login(username='admin', password='adminpw')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_post(self):
        url = '/api/comments/'
        res = self.client.login(username='admin', password='adminpw')
        data = {'content':'new comment', 'post': 1, 'author':1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_patch(self):
        url = '/api/comments/1/'
        res = self.client.login(username='admin', password='adminpw')
        data = {'content':'No, it\'s super hilarious!'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comment = Comment.objects.get(id=1)
        self.assertEqual(comment.content, 'No, it\'s super hilarious!')

    def test_admin_delete(self):
        url = '/api/comments/1/'
        res = self.client.login(username='admin', password='adminpw')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(Tag.objects.all()), 0)
