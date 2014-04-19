from django.conf.urls import patterns, url

from forum import views

urlpatterns = patterns('',
    # ex: /posts
    url(r'^$', views.index, name='index'),
    # ex: /posts/hottest
    url(r'hottest$', views.index_hottest, name='hottest_posts'),
    # ex: /posts/new_post/
    url(r'new_post/$', views.add_post, name='add_post'),
    # ex: /posts/11/edit/
    url(r'^(?P<post_id>\d+)/edit/$', views.add_post, name='edit_post'),

    url(r'^(?P<post_id>\d+)/submit-edit/$', views.add_post, name='submit-edit'),
    # ex: /posts/5/
    url(r'^(?P<post_id>\d+)/$', views.content, name='content'),
    # ex: /posts/17/like
    url(r'^(?P<post_id>\d+)/like/$', views.like, name='like'),
    # ex: /posts/17/delete
    url(r'^(?P<post_id>\d+)/delete/$', views.delete_post, name='delete_post'),
    # ex: /posts/17/comment
    url(r'^(?P<post_id>\d+)/comment/$', views.comment_post, name='comment_post'),
)
