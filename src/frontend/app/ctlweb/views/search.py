#vim: set fileencoding=utf-8
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.template import RequestContext, Template
from django.forms.formsets import formset_factory
from ctlweb.forms import SearchForm, AddSearchForm


def search(request):
    SearchFormset = formset_factory(SearchForm)
    AddSearchFormset = formset_factory(AddSearchForm)
    baseform = SearchFormset(prefix="baseform")
    addform = AddSearchFormset(prefix="addform")
    dict_response = {
            'baseform' : baseform,
            'addform' : addform,
            'STATIC_URL' : '/static/'
            }
    context = Context(dict_response)
    return render_to_response("search.html", context_instance=context)

