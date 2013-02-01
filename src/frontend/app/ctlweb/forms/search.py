#vim: set fileencoding=utf-8
from django import forms
from django.utils.translation import ugettext as _

SEARCH_CATEGORY_CHOICES = (
        ('all', _('Alle Kategorien')),
        ('name', _('Name')),
        ('author', _('Autor')),
        ('keywords', _(u'Schlüsselwort')),
        ('homeserver', _('Server')),
        ('date', _('Datum')),)

class SearchForm(forms.Form):
    Suchtext = forms.CharField(label=_("Suchtext"))
    Kategorie = forms.ChoiceField(choices = SEARCH_CATEGORY_CHOICES,
        label=_("Kategorie"))

class AddSearchForm(forms.Form):
    LOGIC_CHOICES = (
            ('and', 'und'),
            ('and not', 'und nicht'),
            ('or', 'oder'),)
    Bindung = forms.ChoiceField(choices = LOGIC_CHOICES, label=_("Bindung"))
    Suchtext = forms.CharField(label=_("Suchtext"))
    Kategorie = forms.ChoiceField(choices = SEARCH_CATEGORY_CHOICES,
        label=_("Kategorie"))

    class Media:
        js = ('js/dynamic-formset.js',)
