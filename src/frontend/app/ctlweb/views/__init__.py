#vim: set fileencoding=utf-8
from views import *
from search import *
from login import *
from component import *
from userkeyconfig import *
from backend import *
from django import *
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.template import RequestContext, Template 
