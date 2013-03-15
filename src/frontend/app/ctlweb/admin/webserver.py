# vim: set fileencoding=utf-8
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ctlweb.models import Webserver

class WebserverAdmin(admin.ModelAdmin):
    fieldsets = (
            (None, {'fields': ('name', 'domain')}),
            (_('Informations'), {'fields': ('ip',  'port')}),
            )
    list_display = ['name', 'domain', 'ip', 'port']
    search_fields = ('name', 'ip', 'domain', 'port')
    ordering = ['name']

admin.site.register(Webserver, WebserverAdmin)
