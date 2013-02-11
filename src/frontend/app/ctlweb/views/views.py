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
        result = simple_search(query)
        if result.count() == 1:
            return component_detail(request, result[0].pk)
        return lists(request, result, 1)
    return render_to_response("home.html", 
            context_instance=RequestContext(request))

def impressum(request):
    return render_to_response("impressum.html",
            context_instance=RequestContext(request))
