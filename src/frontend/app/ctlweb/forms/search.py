from django import forms

SEARCH_CATEGORY_CHOICES = (
        ('all', 'Alle Kategorien'),
        ('name', 'Name'),
        ('author', 'Autor'),
        ('keywords', 'Schusselwort'),
        ('homeserver', 'Server'),
        ('date', 'Datum'),)

class SearchForm(forms.Form):
    Suchtext = forms.CharField()
    Kategorie = forms.ChoiceField(choices = SEARCH_CATEGORY_CHOICES)

class AddSearchForm(forms.Form):
    LOGIC_CHOICES = (
            ('and', 'und'),
            ('and not', 'und nicht'),
            ('or', 'oder'),)
    Bindung = forms.ChoiceField(choices = LOGIC_CHOICES)
    Suchtext = forms.CharField()
    Kategorie = forms.ChoiceField(choices = SEARCH_CATEGORY_CHOICES)

    class Media:
        js = ('js/dynamic-formset.js',)
