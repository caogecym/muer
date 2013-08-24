from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from apps.joke import urls as joke_urls
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'joke_site.views.home', name='home'),
    # url(r'^joke_site/', include('joke_site.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^joke/', include(joke_urls, namespace="joke")),
    url(r'^account/', include('django_authopenid.urls')),
    url(r'^signin/$', 'django_authopenid.views.signin'),
    url(r'^admin/', include(admin.site.urls)),
)
