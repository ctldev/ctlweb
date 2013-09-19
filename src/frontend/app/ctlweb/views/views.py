#vim: set fileencoding=utf-8
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.template import RequestContext, Template 
from ctlweb.views.lists import *
from ctlweb.views import simple_search

def admin_index(request): 
	return render_to_response("admin/base_site.html", 
			context_instance=RequestContext(request))

def index(request):
    if "search_query" in request.GET:
        return simple_search(request)
    return render_to_response("home.html", 
            context_instance=RequestContext(request))

def components(request): 
    return lists(request)
	
def impressum(request):
    return render_to_response("impressum.html",
            context_instance=RequestContext(request))
