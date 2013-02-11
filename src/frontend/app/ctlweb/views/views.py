#vim: set fileencoding=utf-8
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.template import RequestContext, Template 
from ctlweb.views.util import *
from ctlweb.views.lists import *

def index(request):
    if "search_query" in request.GET:
        query = request.GET.get('search_query','')
        return simple_search(request, query)
    return render_to_response("home.html", 
            context_instance=RequestContext(request))

def components(request): 
    return lists(request)
	
def impressum(request):
    return render_to_response("impressum.html",
            context_instance=RequestContext(request))


