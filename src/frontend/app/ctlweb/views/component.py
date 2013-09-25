#vim: set fileencoding=utf-8
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, Template
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from ctlweb.models import   Components, \
                            Cluster, \
                            Interfaces, \
                            Programmer


def component_detail(request, comp_id):
    """
    Übergibt die Componentdaten ans entsprechende Template weiter
    
    """
    v_user = request.user
    try:
        comp = Components.objects.get(pk=comp_id)
    except Components.DoesNotExist:
        raise Http404
#    if '.' in comp.description:
#        descriptionparts = comp.description.split(". ")
#        short_description = descriptionparts[0] + ". "
#    else:
#        short_description = comp.description[:255]
    short_description = True
    if comp.brief_description == comp.description:
        short_description = None

    can_change = v_user.has_perm('ctlweb.change_components')
    see_description = v_user.has_perm('ctlweb.can_see_description')
    see_homecluster = v_user.has_perm('ctlweb.can_see_homecluster')
    see_ssh_data = v_user.has_perm('ctlweb.can_see_ssh_data')
    see_ci = v_user.has_perm('ctlweb.can_see_ci')
    dict_response = dict()
    dict_response["short"] = short_description
    dict_response["user"] = v_user
    dict_response["component"] = comp
    dict_response["can_change"] = can_change
    dict_response["see_description"] = see_description
    dict_response["see_ssh_data"] = see_ssh_data
    dict_response["see_ci"] = see_ci
    dict_response["see_homecluster"] = see_homecluster
    context = RequestContext(request, dict_response)
    return render_to_response("comp_detail.html", context_instance=context)


def interface(request, int_id):
    
    v_user = request.user
    try: 
        intf = Interfaces.objects.get(pk=int_id)
    except Interfaces.DoesNotExist:
        raise Http404
    
    see_ci = v_user.has_perm('ctlweb.can_see_ci')
    dict_response = dict()
    dict_response["see_ci"] = see_ci
    dict_response["ci"] = intf.ci

    context = RequestContext(request, dict_response)
    response = HttpResponse(content_type='text/plain')
    response = render_to_response("interface.txt", context_instance=context)
    response['Content-Disposition'] = 'attachment; filename=' + intf.name + '.ci'
    #print(dict_response["ci"])
    return response


"""def interface(request): 
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="interface.txt"'
    text_data = (
            ('First row', 'Foo', 'Bar', 'Baz'),
            ('Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"),
        )

    t = loader.get_template('interface.txt')
    c = Context({
        'data': text_data, 
        })
    response.write(t.render(c))
    return response
"""
"""
def interface(request): 
    return render_to_response("interface.txt",
        mimetype="text/plain", context_instance=RequestContext(request))
"""





