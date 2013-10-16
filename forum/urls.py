from django.conf.urls import patterns, url

from forum import views

urlpatterns = patterns('',
    # ex: /posts
    url(r'^$', views.index, name='index'),
    # ex: /posts/hottest
    url(r'hottest$', views.index_hottest, name='hottest_posts'),
    # ex: /posts/new_post/
    url(r'new_post$', views.add_post, name='add_post'),
    # ex: /posts/5/
    url(r'^(?P<post_id>\d+)/$', views.content, name='content'),
    # ex: /posts/17/like
    url(r'^(?P<post_id>\d+)/like/$', views.like, name='like'),
)
