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
          components=None, 
          form=0):
    # components
    #   None = komplettes Verzeichnis
    #   not None = Suchauswahl
    # form:
    #   0 = Verzeichnis
    #   1 = Suche
    
    if form == 0:
        components = Components.objects.all()
        direct_interfaces = Interfaces.objects.all()
    i_components = dict()
    for d in direct_interfaces:
        i_components[d.pk] = Components.objects.filter(component__interfaces = d)
    emails = Programmer.objects.filter(component__in=components).\
        distinct('email').values_list('email')
    userlist= User.objects.filter(email__in=emails)
    dict_response = dict()
    dict_response["form"] = form
    dict_response["d_interfaces"] = direct_interfaces
    dict_response["i_interfaces"] = indirect_interfaces
    dict_response["d_components"] = components
    dict_response["i_components"] = i_components
    dict_response["users"] = userlist
    context = RequestContext(request, dict_response)
    return render_to_response("components.html", context_instance=context)

