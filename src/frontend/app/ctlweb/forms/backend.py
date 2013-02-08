class ComponentRequestForm(forms.Form):
    manifest = forms.FileField()
    creator = forms.EmailField()
    brief_description = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    name = models.CharField()

