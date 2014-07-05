from django.test import TestCase
from django.test.client import Client
from django.template import Context, Template, TemplateSyntaxError
from django.contrib.auth.models import User

from forum.models import Post, Comment
from django.core.paginator import Paginator


class TempTagTestCase(TestCase):
    def setUp(self):
        self.preload = ()
        self.user = User.objects.create_user(username='caogecym', password='42')

    def render_template(self, template, **kwargs):
        """
        Render the given template string with user-defined tag modules
        pre-loaded (according to the class attribute `preload').
        """

        loads = u''
        for load in self.preload:
            loads = u''.join([loads, '{% load ', load, ' %}'])

        template = u''.join([loads, template])
        return Template(template).render(Context(kwargs))

    def test_paginator_empty(self):
        post_list = Post.objects.filter(deleted=False)
        paginator = Paginator(post_list, 1) # Show 10 contacts per page
        posts = paginator.page(1)

        rendered = self.render_template(
            '{% load paginator %}{% paginator 1 %}',
            posts=posts
        )
        self.assertTrue('<span class="current">1</span>' in rendered)

    def test_paginator_multi(self):
        for index in range(0,31):
            Post.objects.create(title='title_%s' % index, content='title_%s' % index, author=self.user)
        post_list = Post.objects.filter(deleted=False)
        paginator = Paginator(post_list, 10) # Show 10 contacts per page
        posts = paginator.page(1)

        rendered = self.render_template(
            '{% load paginator %}{% paginator 1 %}',
            posts=posts
        )
        self.assertTrue('<a href="?page=4"' in rendered)
