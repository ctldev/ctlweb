#vim: set fileencoding=utf-8
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.template import RequestContext, Template 
from ctlweb.views.util import *

def index(request):
    if "search_query" in request.GET:
        simple_search(request.GET.get('search_query',''))
        render_to_response('result.html', 
        context_instance=RequestContext(request))

    return render_to_response("home.html", 
            context_instance=RequestContext(request))

def components(request): 
	return render_to_response("components.html", 
			context_instance=RequestContext(request))
	
def impressum(request):
    return render_to_response("impressum.html",
            context_instance=RequestContext(request))


