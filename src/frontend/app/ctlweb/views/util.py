#vim: set fileencoding=utf-8

from django.db.models import Q
from app.models import Components

def __searchset(searchtext):
    return (Q(name__icontains = searchtext)|
            Q(programmer__icontains = searchtext)|
            Q(description__icontains = searchtext)|
            Q(homeserver__icontains = searchtext)|
            Q(date__icontains = searchtext))

def search(searchtext):
    return Components.objects.filter(__searchset(searchtext))
