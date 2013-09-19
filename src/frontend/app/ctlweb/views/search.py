#vim: set fileencoding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext, Template
from django.forms.formsets import formset_factory
from ctlweb.forms import SearchProBaseForm
from ctlweb.forms import SearchProExtendedForm
from ctlweb.forms import SearchAreaForm
from ctlweb.forms import SEARCH_CATEGORY_CHOICES
from ctlweb.forms import SEARCH_CATEGORIES
from ctlweb.models import Components, Interfaces

def simple_search(request):
    query = request.GET.get('search_query', None)
    interfaces = _get_advanced_searchset('all', query, False, Interfaces.objects)
    components = _get_advanced_searchset('all', query, False)
    return _display_result(request, interfaces, components)

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
        interfaces = _get_advanced_searchset(category, searchtext, regex, 
                                             Interface.objects)
        for form in search_form:
            cleaned_data = form.cleaned_data
            category = cleaned_data['category']
            searchtext = cleaned_data['searchtext']
            regex = cleaned_data['regex']
            bind = cleaned_data['bind']
            components = _combine_querys(components, category, searchtext, 
                                         regex, bind)
            interfaces = _combine_querys(interfaces, category, searchtext, 
                                         regex, bind, Interface.objects)
        return _display_result(request, interfaces, components, searcharea)
    dict_response = {
            'baseform' : search_base_form,
            'addform' : search_form,
            'searchareaform' : area_form,
            'STATIC_URL' : '/static/'
            }
    context = RequestContext(request, dict_response)
    return render_to_response("search.html", context_instance=context)

def _display_result(request, interfaces, components, searcharea='all'):
    interfaces_indirect = Interfaces.objects.none()
    for component in components:
        new_interfaces = component.interfaces_set
        interfaces_indirect = interfaces_indirect | new_interfaces
    interfaces = interfaces.distinct()
    interfaces_indirect = interfaces_indirect.distinct()
    if searcharea == 'components':
        interfaces = Interfaces.objects.none()
    elif searcharea == 'interfaces':
        interfaces_indirect = Interfaces.objects.none()
        components = Components.objects.none()
    return lists(request, interfaces, interfaces_indirect, components, 1)

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
    category = SEARCH_CATEGORIES[filter_target].get(category, None)
    if not category:
        return filter_objects.none()
    if category == 'all':
        searchset = filter_target.none()
        for cat, name in SEARCH_CATEGORY_CHOICES:
            if cat == 'all':
                continue
            searchset = searchset | _get_advanced_searchset(cat, query, regex,
                                                            filter_target)
    else:
        if not regex:
            q = Q(**{'%s__icontains' % category: query})
        else:
            q = Q(**{'%s__iregex' % category: query})
        searchset = filter_target.filter(q)
    return searchset
