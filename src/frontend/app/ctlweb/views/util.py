#vim: set fileencoding=utf-8

from django.db.models import Q
from ctlweb.models import Components, Interfaces
from lists import lists

def __comp_searchset(searchtext):
    return (Q(name__icontains = searchtext)|
            Q(brief_description__icontains = searchtext)|
            Q(programmer__email__iexact = searchtext)|
            Q(homeserver__name__icontains = searchtext)|
            Q(homeserver__ip__icontains = searchtext)|
            Q(version__icontains = searchtext))

def __interface_searchset(searchtext):
    return (Q(name__icontains = searchtext)|
            Q(description__icontains = searchtext))

def simple_search(request, searchtext):
    searched_interfaces = Interfaces.objects.filter(
            __interface_searchset(searchtext))
    searched_components = Components.objects.filter(__comp_searchset(searchtext))
    indirect_interfaces = Interfaces.objects.all()
    for comp in searched_components:
        query = Interfaces.objects.filter(components__name__iexact = comp.name)
        indirect_interfaces = indirect_interfaces | query
    return lists(request, searched_interfaces, indirect_interfaces,
            searched_components, 1)
