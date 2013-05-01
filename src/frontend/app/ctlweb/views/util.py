#vim: set fileencoding=utf-8

from django.db.models import Q
from ctlweb.models import Components, Interfaces
from lists import lists

def __comp_searchset(searchtext):
    """Stellt für jede View die durchsuchbaren Attribute der Components als
    zur Queryset Verfügung."""
    return (Q(name__icontains = searchtext)|
            Q(brief_description__icontains = searchtext)|
            Q(programmer__email__iexact = searchtext)|
            Q(homeserver__name__icontains = searchtext)|
            Q(homeserver__ip__icontains = searchtext)|
            Q(version__icontains = searchtext))

def __interface_searchset(searchtext):
    """Stellt für jede View die durchsuchbaren Attribute der Interfaces als
    zur Queryset Verfügung."""
    return (Q(name__icontains = searchtext)|
            Q(description__icontains = searchtext))

def simple_search(request, searchtext):
    """Global verfügbare einfache Suche die in der Navigation angezeigt
    wird"""
#Verwendung vordefinierter Querysets zur Suche
    searched_interfaces = Interfaces.objects.filter(
            __interface_searchset(searchtext))
    searched_components = Components.objects.filter(__comp_searchset(searchtext))
    searched_components = searched_components.exclude(is_active=False)
#Suche Interfaces deren Components gefunden wurden ohne selbst gefunden zu sein
    indirect_interfaces = Interfaces.objects.none()
    for comp in searched_components:
        indirect_interfaces = indirect_interfaces | Interfaces.objects.all().filter(components__name__iexact = comp.name)
#Distinct auf alle Ergebnisse. Nur auf einige führt zu Kompatibiltätsproblemen
    searched_components = searched_components.distinct()
    searched_interfaces = searched_interfaces.distinct()
    indirect_interfaces = indirect_interfaces.distinct()
    return lists(request, searched_interfaces, indirect_interfaces,
            searched_components, 1)

def generate_page_buttons(prefix, page_count, css_class, page, button_range):
    """generate buttons for pagination"""
    buttons = []
    buttons.append(_generate_button(prefix, "first", css_class, "|&laquo;",
            disabled=(page==1)))
    buttons.append(_generate_button(prefix, "prev", css_class, "&laquo;",
            disabled=(page==1)))

    start = page - (button_range + 1)
    end = page + button_range
    if start < 0:
        start = 0
    if end > page_count:
        end = page_count
    for i in range(start, end):
        buttons.append(_generate_button(prefix, i+1, css_class,
            active=((i+1)==page)))

    buttons.append(_generate_button(prefix, "next", css_class, "&raquo;",
        disabled=(page==page_count)))
    buttons.append(_generate_button(prefix, "last", css_class, "&raquo;|",
        disabled=(page==page_count)))
    return buttons

def _generate_button(prefix, page, css_class, value=None, disabled=False,
        active=False):
    """helper to generate th pagination-buttons"""
    if value == None:
        value = page
    if disabled:
        button = '<li class="disabled">'
    elif active:
        button = '<li class="active">'
    else:
        button = "<li>"
    button +=      """ <a href="javascript:void(0)"
                      class="%s" id="%s%s" """ % (css_class, prefix, page)
    if not disabled and not active:
        button += 'onclick="loadXMLDoc($(this))"'
    button += ">%s</a></li>" % value
    return button
