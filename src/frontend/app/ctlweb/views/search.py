#vim: set fileencoding=utf-8
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.template import RequestContext, Template
from django.forms.formsets import formset_factory
from ctlweb.forms import SearchForm, AddSearchForm, SearchAreaForm
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
    if request.method == 'POST':
#Auslesen der Sucheingaben und initialiseren der Suchergebnisvariablen
        filled_areaform = SearchAreaForm(request.POST, prefix='areaform')
        filled_baseform = SearchFormset(request.POST, prefix='baseform')
        filled_addform = AddSearchFormset(request.POST, prefix='addform')
#Start der Auswertung des Forms zur Bestimmung des Suchegebiet
        if filled_areaform.is_valid():
            searcharea = filled_areaform.cleaned_data['area']
#Initialisierung der Suchvariablen je nachdem in welchem Gebiet gesucht wird.
            if searcharea == 'all' or searcharea == 'components':
#Wenn in dem Gebiet gesucht wird, alle Komponenten in die Variable
                searched_comps = Components.objects.all()
            else :
#Wenn in dem Gebiet nicht gesucht wird, keine Components in die Variable.
                searched_comps = Components.objects.none()
            if searcharea == 'all' or searcharea == 'interfaces':
#Das Gleiche für Interfaces
                searched_interfaces = Interfaces.objects.all()
            else :
                searched_interfaces = Interfaces.objects.none()

#Auswertung des ersten Suchformulars. Für jede Zeile in der Form
            for form in filled_baseform:
                if form.is_valid():
#Auslesen der Eingaben aus dem Form. bind=first, da erster Suchbegriff
                    searchtext = form.cleaned_data['searchtext']
                    category = form.cleaned_data['category']
                    bind = "first"
#Aufruf der Interface- bzw. Componentsuche. Ignoriert leere Suchbegriffe
                    if searcharea == "all" or searcharea == "interfaces" and \
                            searchtext != "":
                        searched_interfaces = search_interfaces(searchtext, 
                                bind, category, searched_interfaces)
                    if searcharea == "all" or searcharea == "components" and \
                            searchtext != "":
                        searched_comps = search_comps(searchtext, bind, 
                                category, searched_comps)
#Basis selbe Auswertung, wie für erste Suchformular für weitere Suchformulare
            for form in filled_addform:
                if form.is_valid():
                    searchtext = form.cleaned_data['searchtext']
                    category = form.cleaned_data['category']
#bind diesmal aus dem Formular gelesen, da unterschiedliche Möglichkeiten.
                    bind = form.cleaned_data['bind']
                    if searcharea == "all" or searcharea == "interfaces" and \
                            searchtext != "":
                        searched_interfaces = search_interfaces(searchtext, 
                                bind, category, searched_interfaces)
                    if searcharea == "all" or searcharea == "components" and \
                            searchtext != "":
                        searched_comps = search_comps(searchtext, bind, 
                                category, searched_comps)
#Entfernen der inaktiven Components aus dem Suchergebnis
            searched_comps = searched_comps.exclude(is_active__icontains =
            "False")
#Bestimmen der Interfaces, die nicht gefunden wurden, aber zu gefundenen
#aber zu gefundenen Komponenten gehören
            indirect_interfaces = Interfaces.objects.none()
            for comp in searched_comps:
                indirect_interfaces = indirect_interfaces | Interfaces.objects.all().filter(components__name__iexact = comp.name)
            indirect_interfaces = indirect_interfaces.distinct()
            searched_interfaces = searched_interfaces.distinct()
            return lists(request, searched_interfaces, indirect_interfaces,
                    searched_comps, 1)
#Erstellen des Suchformulars falls keine Suchanfrage vorhanden ist
    areaform = SearchAreaForm(prefix='areaform')
    baseform = SearchFormset(prefix='baseform')
    addform = AddSearchFormset(prefix='addform')
    dict_response = {
            'baseform' : baseform,
            'addform' : addform,
            'searchareaform' : areaform,
            'STATIC_URL' : '/static/'
            }
    context = RequestContext(request, dict_response)
    return render_to_response("search.html", context_instance=context)

def search_interfaces(searchtext, bind, category, searched_interfaces):
    """Grundlegende Suche der interfaces, die nacheinander für alle
    Verbindungen Suchen startet. Wird von search() mit den Daten des Formulares
    aufgerufen. Der erste Suchdurchgang ist immer eine und-Suche auf alle
    Komponente."""
#Überprüfung welches Bind aktiv
    if bind == "and" or bind == "first":
#Aufruf der passenden Suche
        searched_interfaces = interface_and_search(searchtext,
                category, searched_interfaces)
#Wenn der vorherige Bind nicht der Aktive, Überprüfung auf den Nächsten.
    elif bind == "or":
        searched_interfaces = interface_or_search(searchtext,
                category, searched_interfaces)
#Wenn der vorherige Bind nicht der Aktive, Überprüfung auf den Nächsten.
    elif bind == "and not":
        searched_interfaces = interface_and_not_search(searchtext,
                category, searched_interfaces)
#Rückgabe des modifizierten Suchergebnisses
    return searched_interfaces

def interface_and_search(searchtext, category, searched_interfaces):
    """Modifzierung des Suchergebnisses bei einer interface und Verknüpfung.
    Wird von search_interfaces aufgerufen."""
#Überprüfen in welcher Kategorie gesucht wird.
    if category == 'name':
#Filtern nach allen Interfaces die das Suchkriterium erfüllen.
        searched_interfaces = searched_interfaces.filter(
            name__icontains = searchtext)
    elif category == "keywords":        
        searched_interfaces = searched_interfaces.filter(
            description__icontains = searchtext)
#Sonderfall all-Suche: Es soll ein Interface gefunden werden, dass in einer
#Kategorie dem Suchbegriff entspricht, aber nicht zwangsläufig in jeder.
    elif category == 'all': 
#Einzelnes Suchen nach den Interfaces die in einer Kategorie passen.
        searched_names = searched_interfaces.filter(
            name__icontains = searchtext)
        searched_keywords = searched_interfaces.filter(
            description__icontains = searchtext)
#Zusammenfügen aller gefundenen Interfaces
        searched_interfaces = searched_names | searched_keywords
    return searched_interfaces

def interface_and_not_search(searchtext, category, searched_interfaces):
    """Modifzierung des Suchergebnisses bei einer interface und nicht
    Verknüpfung. Wird von search_interfaces() aufgerufen. Hier ist die all-Suche
    kein Sonderfall"""
#Überprüfung welche Kategorie aktiv. 
    if category == 'name' or category == 'all':
#Entfernen aller Interfaces auf die der Suchbegriff nicht passt.
        searched_interfaces = searched_interfaces.exclude(
            name__icontains = searchtext)
#Da im Falle einer all-Suche alle Schleifen bearbeitet werden if statt elif
    if category == "keywords" or category == 'all':        
        searched_interfaces = searched_interfaces.exclude(
            description__icontains = searchtext)
    return searched_interfaces

def interface_or_search(searchtext, category, searched_interfaces):
    """Modifzierung des Suchergebnisses bei einer interface oder Verknüpfung.
    Wird von search_interfaces() aufgerufen. Hier ist die all-Suche keine
    Ausnahme"""
#Überprüfung welche Kategorie aktiv. 
    if category == 'name' or category == 'all':
#Suche aller Interface auf die der Suchbegriff passt
        search_query = Interfaces.objects.filter(
            name__icontains = searchtext)
#Hinzufügen der gefundenen Ergebnisse zu den Alten
        searched_interfaces = searched_interfaces | search_query
#Da im Falle einer all-Suche alle Schleifen bearbeitet werden if statt elif
    if category == "keywords" or category == 'all':        
        search_query = Interfaces.objects.filter(
                description__icontains = searchtext)
        searched_interfaces = searched_interfaces | search_query
#Distinct um Doppelfindungen durch Zusammenfügen zu vermeiden.
    searched_interfaces = searched_interfaces.distinct()
    return searched_interfaces

def search_comps(searchtext, bind, category, searched_comps):
    """Wie search_interfaces(), allerdings für Komponenten"""
    if bind == "and" or bind == "first":
        searched_comps = and_search(searchtext, category, searched_comps)
    if bind == "or":
        searched_comps = or_search(searchtext, category, searched_comps)
    if bind == "and not":
        searched_comps = and_not_search(searchtext, category, searched_comps)
    return searched_comps

def and_search(searchtext, category, searched_comps):
    """Wie interface_and_search(), allerdings für Komponenten"""
    if category == 'name' or category == 'all':
        searched_comps = searched_comps.filter(
            name__icontains = searchtext)
    elif category == 'keywords':        
        searched_comps = searched_comps.filter(
            brief_description__icontains = searchtext)
    elif category == 'homeserver':        
        searched_comps = searched_comps.filter(
            homeserver__ip__icontains = searchtext)
        searched_comps = searched_comps.filter(
            homeserver__name__icontains = searchtext)
    elif category == 'date':        
        searched_comps = searched_comps.filter(
            date__icontains = searchtext)
    elif category == 'all':
        searched_name = searched_comps.filter(
            name__icontains = searchtext)
        searched_ip = searched_comps.filter(
            homeserver__ip__icontains = searchtext)
        searched_servername = searched_comps.filter(
            homeserver__name__icontains = searchtext)
        searched_date = searched_comps.filter(
            date__icontains = searchtext)
        searched_comps = searched_name | searched_ip | searched_servername |\
        searched_date
    return searched_comps
        
def and_not_search(searchtext, category, searched_comps):
    """Wie interface_and_not_search(), allerdings für Komponenten"""
    if category == 'name' or category == 'all':
        searched_comps = searched_comps.exclude(
            name__icontains = searchtext)
    if category == 'keywords' or category == 'all':        
        searched_comps = searched_comps.exclude(
            brief_description__icontains = searchtext)
    if category == 'homeserver' or category == 'all':
        searched_comps = searched_comps.exclude(
            homeserver__ip__icontains = searchtext)
        searched_comps = searched_comps.exclude(
            homeserver__name__icontains = searchtext)
    if category == 'date' or category == 'all':        
        searched_comps = searched_comps.exclude(
            date__icontains = searchtext)
    return searched_comps

def or_search(searchtext, category, searched_comps):
    """Wie interface_or_search(), allerdings für Komponenten"""
    if category == 'name' or category == 'all':
        search_query = Components.objects.filter(
            name__icontains = searchtext)
        searched_comps = searched_comps | search_query
    if category == 'keywords' or category == 'all':        
        search_query = Components.objects.filter(
            brief_description__icontains = searchtext)
        searched_comps = searched_comps | search_query
    if category == 'homeserver' or category == 'all':        
        search_query = Components.objects.filter(
            homeserver__ip__icontains = searchtext)
        searched_comps = searched_comps | search_query
        search_query = Components.objects.filter(
            homeserver__name__icontains = searchtext)
        searched_comps = searched_comps | search_query
    if category == 'date' or category == 'all':        
        search_query = Components.objects.filter(
            name__icontains = searchtext)
        searched_comps = searched_comps | search_query
        search_query = Components.objects.filter(
            date__icontains = searchtext)
        searched_comps = searched_comps | search_query
    searched_comps = searched_comps.distinct()
    return searched_comps


