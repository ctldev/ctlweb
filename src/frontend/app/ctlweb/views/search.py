#vim: set fileencoding=utf-8
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.template import RequestContext, Template
from django.forms.formsets import formset_factory
from ctlweb.forms import SearchProBaseForm, SearchProExtendedForm, SearchAreaForm
from ctlweb.views.util import *
from ctlweb.models import Components, Interfaces

def search(request):
    """Grundfunktion der Suche. Wenn noch keine Sucheingabe vorhanden ist, wird
    das Suchformular geöffnet. Wenn eine Sucheingabe vorhanden ist, wird diese
    verarbeitet und an die Listenfunktion weitergegeben."""
    search_base_form = SearchProBaseForm(request.POST or None, prefix='baseform')
    search_form = SearchProExtendedForm(request.POST or None, prefix='addform')
    area_form = SearchAreaForm(request.POST or None, prefix='areaform')
    if search_base_form.is_valid() \
            and search_form.is_valid() \
            and area_form.is_valid():
        searcharea = areadorm.cleaned_data['area']
        cleaned_base_data = search_base_form.cleaned_data
        category = cleaned_base_data['category']
        searchtext = cleaned_base_data['searchtext']
        regex = cleaned_base_data['regex']
        components = _get_advanced_searchset(category, searchtext, regex)
        interfaces_direct = _get_advanced_searchset(category, searchtext, 
                regex, Interface.objects)
        for form in search_form:
            cleaned_data = form.cleaned_data
            category = cleaned_data['category']
            searchtext = cleaned_data['searchtext']
            regex = cleaned_data['regex']
            bind = cleaned_data['bind']
            components = _combine_querys(components, category, searchtext, 
                    regex, bind)
            interfaces_direct = _combine_querys(interfaces, category, 
                    searchtext, regex, bind, Interface.objects)
            interfaces_indirect = Interface.objects.none()
        for component in components:
            new_interfaces = component.interfaces_set
            interfaces_indirect = Interfaces_indirect | new_interfaces
        interfaces_indirect = interfaces_indirect.distinct()
        interfaces_direct = interfaces_direct.distinct()
        if searcharea == 'components':
            interfaces_direct = Interfaces.objects.none()
        elif searcharea == 'interfaces':
            interfaces_indirect = interfaces.objects.none()
            components = Components.objects.none()
        return lists(request, interfaces_direct, interfaces_indirect,
                components, 1)
    dict_response = {
            'baseform' : search_base_form,
            'addform' : search_form,
            'searchareaform' : area_form,
            'STATIC_URL' : '/static/'
            }
    context = RequestContext(request, dict_response)
    return render_to_response("search.html", context_instance=context)

def _combine_querys(searchset, category, query, regex, bind,
        filter_target=Components.objects):
    if not query or query == '':
        return searchset
    new_searchset = _get_advanced_searchset(category, query, regex,
            filter_target)
    if new_searchset == filter_target.none():
        return searchset
    ids = new_searchset.values('pk')
    if bind == 'and':
        searchset = searchset.filter(pk__in=ids)
    elif bind == 'and not':
        searchset = searchset.exclude(pk__in=ids)
    elif bind == 'or':
        searchset = searchset | new_searchset
    else:
        raise AttributeError('binding did not match')
    return searchset

def _get_advanced_searchset(category, query, regex,
        filter_target=Components.objects):
    category = ctlweb.forms.SEARCH_CATEGORIES[filter_target][category]
    if not category:
        return filter_objects.none()
    if category == 'all':
        searchset = filter_target.none()
        for cat, name in ctlweb.forms.SEARCH_CATEGORY_CHOICES[1:]:
            searchset = searchset | _get_advanced_searchset(cat, query, regex,
                    filter_target)
    else:
        if not regex:
            q = Q(**{'%s__icontains' % category: query})
        else:
            q = Q(**{'%s__iregex' % category: query})
        searchset = filter_target.filter(q)
    return searchset
