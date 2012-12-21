# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import Context, loader


def index(request): 
    context = Context(get_dict_response(request))
    return render_to_response("index.html",context_instance=context)
