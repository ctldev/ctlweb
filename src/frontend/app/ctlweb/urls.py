#vim: set fileencoding=utf-8
from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template
from app.ctlweb.views import *


urlpatterns = patterns('app.ctlweb.views',
        url(r'^$', 'index', name='index'), 
        url(r'^search/$', 'search', name='search'),
        url(r'^components/$', 'index', name='components'),
        url(r'^components/(?P<comp_id>\d+)/$', 'component_detail', name='component'),
        url(r'^administration/$', 'index', name='administration'),
        url(r'^administration/easy/$', 'index', name='administration_easy'),
        url(r'^administration/advanced/$', 'index', name='administration_advanced'),
        url(r'^impressum/$', 'index', name='impressum'),
)

urlpatterns += patterns('django.contrib.auth.views',
        url(r'^login/$', 'login', name='login'),
        url(r'^logout/$', 'logout', {'next_page': '/'}, name='logout'),
)
