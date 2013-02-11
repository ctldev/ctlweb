#vim: set fileencoding=utf-8
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, Template
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from ctlweb.models import Components, Programmer
from django.contrib.auth.models import User

def lists(request, components=None, form=0):
    # components
    #   None = komplettes Verzeichnis
    #   not None = Suchauswahl
    # form:
    #   0 = Suche/Verzeichnis
    if components == None:
        components = Components.objects.all()
    emails = Programmer.objects.filter(component__in=components).\
        distinct('email').values_list('email')
    userlist= User.objects.filter(email__in=emails)
    dict_response = dict()
    dict_response["components"] = components
    dict_response["users"] = userlist
    context = RequestContext(request, dict_response)
    return render_to_response("components.html", context_instance=context)
