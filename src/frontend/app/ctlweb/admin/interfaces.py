# vim: set fileencoding=utf-8
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ctlweb.models import Interfaces
from ctlweb.admin.components import *

class InterfacesAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name',)}),
        (_('Description'), {'fields': ('description',)}),
        (_('Key'), {'fields': ('key',)}),
        (_('Components'), {'fields': ('components',)}),
    )
    list_display = ['key', 'name']
    search_fields = ('key', 'name', 'description')
    ordering = ['key']

admin.site.register(Interfaces, InterfacesAdmin)
