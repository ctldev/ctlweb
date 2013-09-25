#vim: set fileencoding=utf-8
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.template import RequestContext, Template 
from ctlweb.views.lists import *
from ctlweb.views.search import simple_search


def admin_index(request): 
	return render_to_response("admin/base_site.html", 
			context_instance=RequestContext(request))

def index(request):
    if "search_query" in request.GET:
        return simple_search(request)
    return render_to_response("home.html", 
            context_instance=RequestContext(request))

def components(request): 
    return lists(request)
	
def impressum(request):
    return render_to_response("impressum.html",
            context_instance=RequestContext(request))

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