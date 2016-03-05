from django.conf.urls import patterns, include, url
from django.contrib import admin
from providers.views import *

urlpatterns = patterns('',
    
    # url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'(?P<provider_id>[\w\d]+)/(?P<action>[\w]+)/$', manage_provider, name='manage_provider'),
    url(r'(?P<provider_id>[\w\d]+)/$', manage_provider, name='manage_provider'),
    url(r'$', create_or_get_providers, name='create_or_get_providers'),
    
)