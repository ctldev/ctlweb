#vim: set fileencoding=utf-8
from django import forms
from django.utils.translation import ugettext as _
from ctlweb.models import Components,  Cluster

class ComponentAddForm(forms.ModelForm):
    cluster = forms.ModelMultipleChoiceField(
            queryset=Cluster.objects.exclude(key__exact=None), label=_("Cluster"))
    class Meta:
        model = Components
        exclude = ('date', 'is_active')
