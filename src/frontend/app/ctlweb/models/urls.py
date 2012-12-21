from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template
from ctlweb.views.views import *

urlpatterns = patterns('ctlweb.views.views',
        url(r'^$', 'index', name='index'), 
        
)


