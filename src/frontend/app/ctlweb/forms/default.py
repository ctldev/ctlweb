#vim: set fileencoding=utf-8
from django import forms
from django.utils.translation import ugettext as _
from ctlweb.models import Components, Webserver, Cluster

class ComponentAddForm(forms.ModelForm):
    webserver = forms.ModelMultipleChoiceField(
	      queryset=Webserver.objects.all(), label=_("Webserver"))
    cluster = forms.ModelMultipleChoiceField(
            queryset=Cluster.objects.filter(keys not None), label=_("Cluster"))
    class Meta:
        model = Components
        exclude = ('date', 'is_active')
