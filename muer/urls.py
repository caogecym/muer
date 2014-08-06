import os.path
from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from django.contrib import admin
from forum import views as forum_views
from forum import urls as forum_urls

admin.autodiscover()
APP_PATH = os.path.dirname(__file__)

urlpatterns = patterns('',
    (r'^$', forum_views.index),
    (r'^api/', include(forum_urls)),
    (r'^about/', forum_views.about),
    (r'^home/', forum_views.index),
    #(r'^posts/', include(forum_urls, namespace="forum")),
    #(r'^search/', forum_views.search),
    #(r'^tags/$', forum_views.tags),
    #(r'^tags/(?P<tag>[^/]+)/$', forum_views.tag),
    (r'^login/$', login),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page':'/'}),
    (r'^signup/$', 'forum.views.register'),

    # wechat interface
    (r'^wechat/', forum_views.Weixin.as_view()),

    url(r'^admin/', include(admin.site.urls)),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
