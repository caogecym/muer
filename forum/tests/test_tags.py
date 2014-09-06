from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from forum.models import Tag

class TagTests(APITestCase):
    def setUp(self):
        normal_user_0 = User.objects.create_user(username='caogecym', password='42')
        User.objects.create_user(username='caogecym1', password='421')
        super_user = User.objects.create_user(username='admin', password='adminpw')
        super_user.is_staff = True
        super_user.save()

        Tag.objects.create(name="animal", author=normal_user_0)
        print "In method %s" % self._testMethodName

    def test_unlogged_in_get_list(self):
        url = '/api/tags'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unlogged_in_get_detail(self):
        url = '/api/tags/1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unlogged_in_post(self):
        url = '/api/tags'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unlogged_in_put(self):
        url = '/api/tags/1'
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unlogged_in_delete(self):
        url = '/api/tags/1'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_normal_user_get_list(self):
        url = '/api/tags'
        self.client.login(username='caogecym', password='42')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_normal_user_get_detail(self):
        url = '/api/tags/1'
        self.client.login(username='caogecym', password='42')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_normal_user_post(self):
        url = '/api/tags'
        self.client.login(username='caogecym', password='42')
        data = {'name': 'new_joke', 'author': 1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_normal_user_put(self):
        url = '/api/tags/1'
        self.client.login(username='caogecym', password='42')
        data = {'name': 'new_joke', 'author': 1}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_normal_user_delete(self):
        url = '/api/tags/1'
        self.client.login(username='caogecym', password='42')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_get_list(self):
        url = '/api/tags'
        self.client.login(username='admin', password='adminpw')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_get_detail(self):
        url = '/api/tags/1'
        self.client.login(username='admin', password='adminpw')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_post(self):
        url = '/api/tags'
        self.client.login(username='admin', password='adminpw')
        data = {'name': 'new_joke', 'author': 1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_put(self):
        url = '/api/tags/1'
        self.client.login(username='admin', password='adminpw')
        data = {'name': 'updated_joke'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tag = Tag.objects.get(id=1)
        self.assertEqual(tag.name, 'updated_joke')

    def test_admin_delete(self):
        url = '/api/tags/1'
        self.client.login(username='admin', password='adminpw')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(Tag.objects.all()), 0)
