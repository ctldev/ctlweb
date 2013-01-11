from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template
from app.ctlweb.views import *

urlpatterns = patterns('app.ctlweb.views',
        url(r'^$', 'index'), 
        
)


