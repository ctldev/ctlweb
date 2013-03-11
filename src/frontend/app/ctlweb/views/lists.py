#vim: set fileencoding=utf-8
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, Template
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from ctlweb.models import Components, Interfaces, Programmer
from django.contrib.auth.models import User

def lists(request, 
          direct_interfaces=None, 
          indirect_interfaces=None,
          s_components=None, 
          form=0):
    # form:
    #   0 = Verzeichnis
    #   1 = Suche
    
    v_user = request.user
    programmer = Programmer.objects.all().order_by('email')
    emails = Programmer.objects.distinct('email').values_list('email')
    u_programmer = User.objects.filter(email__in=emails)
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
        s_components = s_components.order_by('name')
    if form == 0:
        direct_interfaces = Interfaces.objects.all().order_by('name')
#    emails = ""
#    if components is not None:
#        emails = Programmer.objects.filter(component__in=components).\
#                distinct('email').values_list('email')
#TODO Überarbeiten
#    if direct_interfaces is not None:
#        for d in direct_interfaces:
#            i_components[d.pk] = Components.objects.filter(\
#                    component__interfaces = d)
#            emails += Programmer.objects.\
#                    filter(component__in=i_components[d.pk]).\
#                    distinct('email').values_list('email')
#    userlist= User.objects.filter(email__in=emails)
    dict_response["user"] = v_user
    dict_response["form"] = form
    dict_response["d_interfaces"] = direct_interfaces
    dict_response["i_interfaces"] = indirect_interfaces
    dict_response["search_components"] = s_components
    dict_response["programmer"] = programmer
    dict_response["u_programmer"] = u_programmer
#    dict_response["users"] = userlist
    context = RequestContext(request, dict_response)
    return render_to_response("components.html", context_instance=context)

