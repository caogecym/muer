from django.conf.urls import patterns, url

from forum import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    # ex: /joke/5/
    url(r'^(?P<joke_id>\d+)/$', views.content, name='content'),
    # ex: /joke/17/like
    url(r'^(?P<joke_id>\d+)/like/$', views.like, name='like'),
)
