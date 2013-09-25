#vim: set fileencoding=utf-8
from django import forms
class ComponentRequestForm(forms.Form):
    manifest = forms.FileField()

class ComponentDeleteForm(forms.Form):
    exe_hash = forms.CharField()
