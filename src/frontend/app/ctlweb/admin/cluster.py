# vim: set fileencoding=utf-8
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ctlweb.models import Cluster

class ClusterAdmin(admin.ModelAdmin):
    """
    Umfasst die Clustereinstellungen für das Backend

    """
    fieldsets = (
            (None, {'fields': ('domain',)}),
            (_('Informations'), {'fields': ('ip', 'port')}),
            (_('Key'), {'fields': ('key',)}),
            )
    list_display = ['domain', 'ip', 'port']
    search_fields = ('domain', 'ip', 'port')
    ordering = ['domain']

admin.site.register(Cluster, ClusterAdmin)

