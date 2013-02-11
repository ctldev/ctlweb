#vim: set fileencoding=utf-8
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.template import RequestContext, Template
from django.forms.formsets import formset_factory
from ctlweb.forms import SearchForm, AddSearchForm
from ctlweb.views.util import *
from ctlweb.models import Components

def advanced_search(searchtext, searched_comps):
    if bind == "and":
        searched_comps = and_search(searchtext, searched_comps)

def and_search(searchtext, searched_comps):
    if category == 'name':
        searched_comps = searched_comps.filter(
            name__icontains = searchtext)
    elif category == "keywords":        
        searched_comps = searched_comps.filter(
            brief_description__icontains = searchtext)
    elif category == "homeserver":        
        searched_comps = searched_comps.filter(
            homeserver__ip__icontains = searchtext)
        searched_comps = searched_comps.filter(
            homeserver__name__icontains = searchtext)
    elif category == "homeserver":        
        searched_comps = searched_comps.filter(
            homeserver__ip__icontains = searchtext)
    elif category == "date":        
        searched_comps = searched_comps.filter(
            date__icontains = searchtext)

def search(request):
    SearchFormset = formset_factory(SearchForm)
    AddSearchFormset = formset_factory(AddSearchForm)
    if 'baseform-0-searchtext' in request.POST:
        print request.POST.get('baseform-0-searchtext','fail')
        filled_baseform = SearchFormset(request.POST, request.FILES,
                prefix='baseform')
        filled_addform = AddSearchFormset(request.POST, request.FILES,
                prefix='addform')
        print filled_baseform
        searched_comps = Components.objects
        for form in filled_baseform:
            searched comps = advanced_search(searchtext, searched_comps)
        for form in filled_addform:
            searched_comps = advanced_search(searchtext, searched_comps)
    baseform = SearchFormset(prefix="baseform")
    addform = AddSearchFormset(prefix="addform")
    dict_response = {
            'baseform' : baseform,
            'addform' : addform,
            'STATIC_URL' : '/static/'
            }
    context = Context(dict_response)
    return render_to_response("search.html", context_instance=context)

