#vim: set fileencoding=utf-8
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.template import RequestContext, Template
from django.forms.formsets import formset_factory
from ctlweb.forms import UserkeyAddForm, CurrentUserkeyForm
from ctlweb.views.util import *
from ctlweb.models import Userkeys
from django.contrib.auth.models import User


def userkey_main(request):

    """Grundfunktion der Suche. Wenn noch keine Sucheingabe vorhanden ist, wird
    das Suchformular geöffnet. Wenn eine Sucheingabe vorhanden ist, wird diese
    verarbeitet und an die Listenfunktion weitergegeben."""
    UserkeyFormset = formset_factory(CurrentUserkeyForm)
    logged_user = request.user
    if request.method == 'POST':
    	current_keys = Userkeys.objects.all().filter(
            user__username__icontains = logged_user.username)
        filled_currentform = UserkeyFormset(request.POST, prefix='current')
        filled_addform = UserkeyAddForm(request.POST, prefix = 'add')
        for form in filled_currentform:
            if form.is_valid():
                old_userkey = form.cleaned_data.get('current_userkey')
                if old_userkey != None:
                	delete_key = current_keys.filter(key__icontains = old_userkey)
                	delete_key.delete()
        if filled_addform.is_valid():
            new_userkey = filled_addform.cleaned_data['new_userkey']
            new_userkey_data = Userkeys(user=logged_user, key=new_userkey)
            new_userkey_data.save()
        current_key_list = []
        for key_model in current_keys:
            current_key_list.append({'current_userkey': key_model.key,
                'deletechoice': False})
        currentuserkeyform=UserkeyFormset(prefix='current', initial=current_key_list)
        adduserkeyform = UserkeyAddForm(prefix = 'add')
        dict_response = {
            'currentform' : currentuserkeyform,
            'addform' : adduserkeyform,
            'STATIC_URL' : '/static/'
        }
        context = RequestContext(request, dict_response)
        return render_to_response("userkey.html", context_instance=context)

    current_keys = Userkeys.objects.all().filter(
        user__username__icontains = logged_user.username)
    current_key_list = []
    for key_model in current_keys:
        current_key_list.append({'current_userkey': key_model.key,
            'deletechoice': False})
    currentuserkeyform=UserkeyFormset(prefix='current', initial=current_key_list)
    adduserkeyform = UserkeyAddForm(prefix = 'add')
    dict_response = {
        'currentform' : currentuserkeyform,
        'addform' : adduserkeyform,
        'STATIC_URL' : '/static/'
        }
    context = RequestContext(request, dict_response)
    return render_to_response("userkey.html", context_instance=context)


