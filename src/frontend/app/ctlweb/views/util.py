#vim: set fileencoding=utf-8

from django.db.models import Q
from ctlweb.models import Components

def __searchset(searchtext):
    return (Q(name__icontains = searchtext)|
            Q(programmer__iexact = searchtext)|
            Q(description__icontains = searchtext)|
            Q(homeserver__name__icontains = searchtext)|
            Q(homeserver__ip__icontains = searchtext)|
            Q(date__icontains = searchtext))

def simple_search(searchtext):
    return Components.objects.filter(__searchset(searchtext))
