from django import forms

class SearchForm(forms.Form):
    CATEGORY_CHOICES = (
            ('all', 'Alle Kategorien'),
            ('name', 'Name'),
            ('author', 'Autor'),
            ('keywords', 'Schusselwort'),)
    Suchtext = forms.CharField()
    Kategorie = forms.ChoiceField(choices = CATEGORY_CHOICES)

class AddSearchForm(forms.Form):
    CATEGORY_CHOICES = (
            ('all', 'Alle Kategorien'),
            ('name', 'Name'),
            ('author', 'Autor'),
            ('keywords', 'Schusselwort'),)
    LOGIC_CHOICES = (
            ('and', 'und'),
            ('and not', 'und nicht'),
            ('or', 'oder'),)
    Bindung = forms.ChoiceField(choices = LOGIC_CHOICES)
    Suchtext = forms.CharField()
    Kategorie = forms.ChoiceField(choices = CATEGORY_CHOICES)
