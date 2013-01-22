from django import forms
from django.utils.translation import ugettext as _
from ctlweb.models import components

class ComponentAddForm(ModelForm):
    #TODO welche Webserver, welche CLuster sollen nur angezeigt werden?
    webserver = forms.ModelMultipleChoiceField(
	      queryset=Webserver.objects.all()), label=_("Webserver"))
    cluster = forms.ModelMultileChoiceField(
            queryset=Cluster.objects.all()), label=_("Cluster"))
    class Meta:
        model = components
	    exclude = ('date', 'is_active')
