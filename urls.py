from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from forum import urls as forum_urls
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^posts/', include(forum_urls, namespace="forum")),
    url(r'^account/', include('django_authopenid.urls')),
    url(r'^signin/$', 'django_authopenid.views.signin'),
    url(r'^admin/', include(admin.site.urls)),
)
