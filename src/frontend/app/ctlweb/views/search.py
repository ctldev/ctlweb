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

def search(request):
    """Grundfunktion der Suche. Wenn noch keine Sucheingabe vorhanden ist, wird
    das Suchformular geöffnet. Wenn eine Sucheingabe vorhanden ist, wird diese
    verarbeitet und an die Listenfunktion weitergegeben."""
    #Erstellung der Formsets aus dem Import der forms
    SearchFormset = formset_factory(SearchForm)
    AddSearchFormset = formset_factory(AddSearchForm)
    #Abfrage ob schon eine Sucheingabe vorhanden ist.
    if 'baseform-0-searchtext' in request.POST:
        #Auslesen der Sucheingaben und initialiseren der Suchergebnisvariablen
        filled_baseform = SearchFormset(request.POST, prefix='baseform')
        filled_addform = AddSearchFormset(request.POST, prefix='addform')
        searched_comps = Components.objects.all()
        searched_interfaces = Interfaces.objects.all
        #Auswertung der Forms mit Unterfunktionen für Component und Interface
        for form in filled_baseform:
            searched_interfaces = search_interface(searchtext,
                    searched_interfaces)
            searched_comps = search_comps(searchtext, searched_comps)
        for form in filled_addform:
            searched_interfaces = search_interface(searchtext,
                    searched_interfaces)
            searched_comps = search_comps(searchtext, searched_comps)
        print "Sucherückgabe" + searched_interfaces + searched_components
        #Weiterleiten der nun gefüllten Ergebnisvariablen an die Listenfunktion
        return lists(request, searched_interfaces, indirect_interfaces,
                searched_components, 1)
    #Erstellen des Suchformulars falls keine Suchanfrage vorhanden ist
    baseform = SearchFormset(prefix="baseform")
    addform = AddSearchFormset(prefix="addform")
    dict_response = {
            'baseform' : baseform,
            'addform' : addform,
            'STATIC_URL' : '/static/'
            }
    context = Context(dict_response)
    return render_to_response("search.html", context_instance=context)

def search_interfaces(searchtext, searched_interfaces):
    """Grundlegende Suche der interfaces, die nacheinander für alle
    Verbindungen Suchen startet"""
    if bind == "and":
        searched_interfaces = interface_and_search(searchtext,
                searched_interfaces)
    if bind == "or":
        searched_interfaces = interface_or_search(searchtext,
                searched_interfaces)
    if bind == "and not":
        searched_interfaces = interface_and_not_search(searchtext,
                searched_interfaces)
    return searched_interfaces

def interface_and_search(searchtext, searched_interfaces):
    """Modifzierung des Suchergebnisses bei einer interface und Verknüpfung"""
    if category == 'name':
        searched_interfaces = searched_interfaces.filter(
            name__icontains = searchtext)
    elif category == "description":        
        searched_interfaces = searched_interfaces.filter(
            description__icontains = searchtext)
    return searched_interfaces

def interface_and_not_search(searchtext, searched_interfaces):
    """Modifzierung des Suchergebnisses bei einer interface und nicht Verknüpfung"""
    if category == 'name':
        searched_interfaces = searched_interfaces.exclude(
            name__icontains = searchtext)
    elif category == "description":        
        searched_interfaces = searched_interfaces.exclude(
            description__icontains = searchtext)
    return searched_interfaces

def interfaces_or_search(searchtext, searched_interfaces):
    """Modifzierung des Suchergebnisses bei einer interface oder Verknüpfung"""
    if category == 'name':
        search_query = Components.objects.filter(
            name__icontains = searchtext)
        searched_interfaces = searched_interfaces | search_query
    elif category == "keywords":        
        search_query = Components.objects.filter(
            brief_description__icontains = searchtext)
        searched_interfaces = searched_interfaces | search_query
    return searched_interfaces

def search_comps(searchtext, searched_comps):
    """Grundlegende Suche der components, die nacheinander für alle
    Verbindungen Suchen startet"""
    if bind == "and":
        searched_comps = and_search(searchtext, searched_comps)
    if bind == "or":
        searched_comps = or_search(searchtext, searched_comps)
    if bind == "and not":
        searched_comps = and_not_search(searchtext, searched_comps)
    return searched_comps

def and_search(searchtext, searched_comps):
    """Modifzierung des Suchergebnisses bei einer component und Verknüpfung"""
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
    return searched_comps
        
def and_not_search(searchtext, searched_comps):
    """Modifzierung des Suchergebnisses bei einer component und nicht Verknüpfung"""
    if category == 'name':
        searched_comps = searched_comps.exclude(
            name__icontains = searchtext)
    elif category == "keywords":        
        searched_comps = searched_comps.exclude(
            brief_description__icontains = searchtext)
    elif category == "homeserver":        
        searched_comps = searched_comps.exclude(
            homeserver__ip__icontains = searchtext)
        searched_comps = searched_comps.exclude(
            homeserver__name__icontains = searchtext)
    elif category == "homeserver":        
        searched_comps = searched_comps.exclude(
            homeserver__ip__icontains = searchtext)
    elif category == "date":        
        searched_comps = searched_comps.exclude(
            date__icontains = searchtext)
    return searched_comps

def or_search(searchtext, searched_comps):
    """Modifzierung des Suchergebnisses bei einer component und Verknüpfung"""
    if category == 'name':
        search_query = Components.objects.filter(
            name__icontains = searchtext)
        searched_comps = searched_comps | search_query
    elif category == "keywords":        
        search_query = Components.objects.filter(
            brief_description__icontains = searchtext)
        searched_comps = searched_comps | search_query
    elif category == "homeserver":        
        search_query = Components.objects.filter(
            homeserver__ip__icontains = searchtext)
        searched_comps = searched_comps | search_query
        search_query = Components.objects.filter(
            homeserver__name__icontains = searchtext)
        searched_comps = searched_comps | search_query
    elif category == "homeserver":        
        search_query = Components.objects.filter(
            name__icontains = searchtext)
        searched_comps = searched_comps | search_query
        searched_comps = searched_comps.filter(
            homeserver__ip__icontains = searchtext)
    elif category == "date":        
        search_query = Components.objects.filter(
            name__icontains = searchtext)
        searched_comps = searched_comps | search_query
        searched_comps = searched_comps.filter(
            date__icontains = searchtext)
    return searched_comps


