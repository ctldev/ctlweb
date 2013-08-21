#vim: set fileencoding=utf-8
from django import forms
from django.utils.translation import ugettext as _

SEARCH_CATEGORY_CHOICES = (
        ('all', _('Alle Kategorien')),
        ('name', _('Name')),
        ('author', _('Autor')),
        ('keywords', _(u'Schlüsselwort')),
        ('date', _('Datum')),)

class SearchAreaForm(forms.Form):
    SEARCHAREA_CHOICES = (
            ('all', _('Komponenten und Interfaces')),
            ('components', _('Komponenten')),
            ('interfaces', _('Interfaces')),)
    area = forms.ChoiceField(choices = SEARCHAREA_CHOICES,
            label=_('Suchgebiet'))

class SearchForm(forms.Form):
    searchtext = forms.CharField(label=_("Suchtext"))
    category = forms.ChoiceField(choices = SEARCH_CATEGORY_CHOICES,
        label=_("Kategorie"))

class AddSearchForm(forms.Form):
    LOGIC_CHOICES = (
            ('and', _('und')),
            ('and not', _('und nicht')),
            ('or', _('oder')),)
    bind = forms.ChoiceField(choices = LOGIC_CHOICES, label=_("Bindung"))
    searchtext = forms.CharField(label=_("Suchtext"))
    category = forms.ChoiceField(choices = SEARCH_CATEGORY_CHOICES,
        label=_("Kategorie"))

    class Media:
        js = ('js/dynamic-formset.js',)
