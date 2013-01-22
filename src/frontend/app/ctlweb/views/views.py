#vim: set fileencoding=utf-8
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.template import RequestContext, Template 

def index(request):
    
    return render_to_response("home.html", context_instance=RequestContext(request))
