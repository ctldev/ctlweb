#vim: set fileencoding=utf-8
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.template import RequestContext, Template 

def login(request):
    
    return render_to_response("login.html", context_instance=RequestContext(request))