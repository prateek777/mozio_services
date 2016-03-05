from django.conf.urls import patterns, include, url
from django.contrib import admin
from service_areas.views import *

urlpatterns = patterns('',
    
    url(r'(?P<polygon_id>[\w\d]+)/(?P<action>[\w]+)/$', manage_polygon, name='manage_polygon'),
    url(r'(?P<polygon_id>[\w\d]+)/$', manage_polygon, name='manage_polygon'),
    url(r'overlap/detailed$', overlapping_polygons_detailed, name='overlapping_polygons_detailed'),
    url(r'overlap$', overlapping_polygons, name='overlapping_polygons'),
    url(r'$', create_or_get_polygons, name='create_or_get_polygons'),
    
)
