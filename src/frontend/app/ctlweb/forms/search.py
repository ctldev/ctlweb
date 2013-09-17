#vim: set fileencoding=utf-8
from django import forms
from django.forms.formsets import formset_factory
from django.utils.translation import ugettext as _
from ctlweb.models import Components, Interfaces

SEARCH_CATEGORY_CHOICES = (
        ('all', _('Alle Kategorien')),
        ('name', _('Name')),
        ('programmer', _('Autor')),
        ('description', _(u'Schlüsselwort')),
    )

SEARCH_CATEGORIES = {
        Components.objects: {
            'all': 'all',
            'name': 'components_cluster__name',
            'programmer': 'programmer__email',
            'description': 'description',
        },
        Interfaces.objects: {
            'all': 'all',
            'name': 'name',
            'programmer': None,
            'description': None,
        },
    }

class SearchAreaForm(forms.Form):
    SEARCHAREA_CHOICES = (
            ('all', _('Komponenten und Interfaces')),
            ('components', _('Komponenten')),
            ('interfaces', _('Interfaces')),)
    area = forms.ChoiceField(choices = SEARCHAREA_CHOICES,
            label=_('Suchgebiet'))

class SearchProBaseForm(forms.Form):
    searchtext = forms.CharField(label=_("Suchtext"), required=False)
    category = forms.ChoiceField(choices = SEARCH_CATEGORY_CHOICES,
        label=_("Kategorie"))
    regex = forms.BooleanField(required=False, 
            label=u'<a href="http://perldoc.perl.org/perlrequick.html">Regex</a>')

    class Media:
        js = ('js/dynamic-formset.js',)

class SearchProForm(SearchProBaseForm):
    LOGIC_CHOICES = (
            ('and', _('und')),
            ('and not', _('und nicht')),
            ('or', _('oder')),)
    bind = forms.ChoiceField(choices=LOGIC_CHOICES, label=_("Bindung"))

SearchProExtendedForm = formset_factory(SearchProForm)
