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

class CurrentUserkeyForm(forms.Form):
	deletechoice = forms.BooleanField(label=_('Entfernen?'))
	current_userkey = forms.CharField(widget=forms.Textarea(attrs={'rows':5, 'cols':200, 'readonly':True}))

class UserkeyAddForm(forms.Form):
    new_userkey = forms.CharField(label=_(u'Neuer Userkey'),
    	widget=forms.Textarea(attrs={'rows':5, 'cols':200}))
