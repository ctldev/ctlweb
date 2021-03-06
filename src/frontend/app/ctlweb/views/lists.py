#vim: set fileencoding=utf-8
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, Template
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from ctlweb.models import Components, Interfaces, Programmer
from django.contrib.auth.models import User
from django.conf import settings
import util

def lists(request, 
          direct_interfaces=None, 
          indirect_interfaces=None,
          s_components=None, 
          form=0):
    """
    Die Methode stellt die äußere Form der Componentdarstellungsseiten dar.

    """
    # form:
    #   0 = Verzeichnis
    #   1 = Suche

    if "ajax" in request.GET and request.GET["ajax"] == "true":
        return new_page(request, direct_interfaces, indirect_interfaces,
                s_components, form)
    
    v_user = request.user
    dict_response = dict()
    dict_response["user"] = v_user
    dict_response["form"] = form
    dict_response["post_data"] = request.POST.urlencode()
    context = RequestContext(request, dict_response)
    return render_to_response("components.html", context_instance=context)

def new_page(request,
          direct_interfaces=None, 
          indirect_interfaces=None,
          s_components=None, 
          form=0):
    """ this method handles the ajax-requests to dynamically reloading the new
    pages"""
    # form:
    #   0 = Verzeichnis
    #   1 = Suche
    
    v_user = request.user
    dict_response = dict()
    if direct_interfaces == None :
        direct_interfaces = Interfaces.objects.none()
    else :
        direct_interfaces = direct_interfaces.order_by('name')
    if indirect_interfaces == None :
        indirect_interfaces = Interfaces.objects.none()
    else :
        for d in direct_interfaces:
            indirect_interfaces = indirect_interfaces.exclude(name = d.name)
        indirect_interfaces = indirect_interfaces.order_by('name')  
    if s_components == None :
        s_components = Components.objects.none()
    else :
        s_components = s_components.order_by('names').distinct()
    s_components = s_components.exclude(is_active=False)
    if form == 0:
        direct_interfaces = Interfaces.objects.all().order_by('name')
        s_components = \
                Components.objects.filter(is_active=True).order_by('names')
    interface_page_range = settings.PAGINATION_PAGE_RANGE_INTERFACES
    components_page_range = settings.PAGINATION_PAGE_RANGE_COMPONENTS
    button_range = settings.PAGINATION_BUTTON_RANGE
    interfaces = direct_interfaces | indirect_interfaces

    # get active pagenumbers
    inter_page = request.GET.get('di_page', 1)
    if not inter_page == "last":
        try:
            inter_page = int(inter_page)
        except ValueError:
            inter_page = 1
    comp_page = request.GET.get('di_co_page', 1)
    if not comp_page == "last":
        try:
            comp_page = int(comp_page)
        except ValueError:
            comp_page = 1
    s_comp_page = request.GET.get('co_page', 1)
    if not s_comp_page == "last":
        try:
            s_comp_page = int(s_comp_page)
        except ValueError:
            s_comp_page = 1

    for inter in interfaces:
        inter.is_direct = (inter in direct_interfaces)
        components = inter.components.all()
        if not inter.is_direct:
            for c in inter.components.all():
                if c not in s_components:
                    components = components.exclude(pk=c.pk)
        components = components.exclude(is_active=False)
        components = components.order_by('names').distinct()
        pn_comp = Paginator(components, components_page_range)
        if comp_page == "last":
            comp_page = pn_comp.num_pages
        try:
            paged_components = pn_comp.page(comp_page)
        except (EmptyPage, InvalidPage):
            paged_components = pn_comp.page(pn_comp.num_pages)
        inter.paged_components = paged_components
        inter.page_buttons = util.generate_page_buttons("di_co_button_",
                pn_comp.num_pages, "di_co_page", comp_page, button_range)

    pn_interfaces = Paginator(interfaces, interface_page_range)
    if inter_page == "last":
        inter_page = pn_interfaces.num_pages
    try:
        paged_interfaces = pn_interfaces.page(inter_page)
    except (EmptyPage, InvalidPage):
        paged_interfaces = pn_interfaces.page(pn_interfaces.num_pages)

    interfaces_page_buttons = util.generate_page_buttons("di_button_", 
            pn_interfaces.num_pages, "di_page", inter_page, button_range)
    pn_comp = Paginator(s_components, components_page_range)
    if s_comp_page == "last":
        s_comp_page = pn_comp.num_pages
    try:
        s_paged_components = pn_comp.page(s_comp_page)
    except (EmptyPage, InvalidPage):
        s_paged_components = pn_comp.page(pn_comp.num_pages)
    s_components_page_buttons = util.generate_page_buttons("co_button_",
            pn_comp.num_pages, "co_page", s_comp_page, button_range)
    view = request.GET.get('view', '')

    see_ci = v_user.has_perm('ctlweb.can_see_ci')
    see_description = v_user.has_perm('ctlweb.can_see_description')
    dict_response["user"] = v_user
    dict_response["form"] = form
    dict_response["interfaces"] = paged_interfaces
    dict_response["search_components"] = s_components
    dict_response["paged_components"] = s_paged_components
    dict_response["interface_page_buttons"] = interfaces_page_buttons
    dict_response["s_components_page_buttons"] = s_components_page_buttons
    dict_response["post_data"] = request.POST.urlencode()
    dict_response["view"] = view
    dict_response["see_ci"] = see_ci
    dict_response["see_description"]= see_description

    if "search_query" in request.GET:
        dict_response["searchquery"] = request.GET.get('search_query', None)

    context = RequestContext(request, dict_response)
    return render_to_response("components_new_page.html",
            context_instance=context)
