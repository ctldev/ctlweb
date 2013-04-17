# vim: set fileencoding=utf-8
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ctlweb.models import Interfaces, Interfaces_Components

class Components_Inline(admin.StackedInline):
    model = Interfaces_Components
    extra = 0

class InterfacesAdmin(admin.ModelAdmin):
    """
    Umfasst die Interfaceeinstellungen fürs Backend

    """
    fieldsets = (
        (None, {'fields': ('name',)}),
        (_('Description'), {'fields': ('description',)}),
        (_('Key'), {'fields': ('key',)}),
    )
    list_display = ['key', 'name']
    search_fields = ('key', 'name', 'description')
    ordering = ['key']
    inlines = [Components_Inline,]

admin.site.register(Interfaces, InterfacesAdmin)
