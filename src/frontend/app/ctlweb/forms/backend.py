#vim: set fileencoding=utf-8
from django import forms
class ComponentRequestForm(forms.Form):
    manifest = forms.FileField()

class InterfaceRequestForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    hash = forms.CharField()