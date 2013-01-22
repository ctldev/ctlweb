# vim: set fileencoding=utf-8
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, Template
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from ctlweb.models import components, webserver, cluster

def component_detail(request, comp_id):
    v_user = request.user
    try:
        comp = components.objects.get(pk=comp_id)
    except components.DoesNotExist:
        raise Http404
    if v_user.email == comp.programmer and 'edit' in request.POST \
            and v_user.has_perm('ctlweb.change_components'):
        #TODO form zum Editieren/Einfügen schreiben & hier aufrufen
        pass
    homeserver = comp.components_webservers_set.order_by('name')
    homecluster = comp.components_clusters_set.order_by('domain')

    template = loader.get_template("comp_detail.html")

    can_change = v_user.has_perm('ctlweb.change_components')
    see_path = v_user.has_perm('ctlweb.can_see_path')
    see_description = v_user.has_perm('components.can_see_description')
    see_code = v_user.has_perm('ctlweb.can_see_code')
    see_homecluster = v_user.has_perm('ctlweb.can_see_homecluster')
    see_homeserver = v_user.has_perm('ctlweb.can_see_homeserver')
    dict_response = get_dict_response(request)
    dict_response["component"] = com
    dict_response["homeserver"] = homeserver
    dict_response["homecluster"] = homecluster
    dict_response["can_change"] = can_change
    dict_response["see_path"] = see_path
    dict_response["see_description"] = see_description
    dict_response["see_code"] = see_code
    dict_response["see_homecluster"] = see_homecluster
    dict_response["see_homeserver"] = see_homeserver

    context = Context(dict_response)
    response = HttpResponse(template.render(context))
    return response
