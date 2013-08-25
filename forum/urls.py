from django.conf.urls import patterns, url

from forum import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    # ex: /posts/5/
    url(r'^(?P<post_id>\d+)/$', views.content, name='content'),
    # ex: /posts/17/like
    url(r'^(?P<post_id>\d+)/like/$', views.like, name='like'),
)
