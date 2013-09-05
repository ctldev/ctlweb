# vim: set fileencoding=utf-8
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count

from ctlweb.models import Cluster
from ctlweb.models import Components_Cluster

class Components_Inline(admin.StackedInline):
    model = Components_Cluster
    extra = 0

class ClusterAdmin(admin.ModelAdmin):
    """
    Umfasst die Clustereinstellungen für das Backend

    """
    fieldsets = (
            (None, {'fields': ('domain',)}),
            (_('Informations'), {'fields': ('ip', 'username', 'port')}),
            (_('Key'), {'fields': ('key',)}),
            )
    list_display = ['domain', 'ip', 'port', 'counter']
    search_fields = ('domain', 'ip', 'port')
    ordering = ['domain']
    inlines = [Components_Inline,]

    def queryset(self, request):
        return Cluster.objects.annotate(comp_count=Count('components'))

    def counter(self, obj):
        return obj.comp_count
    counter.admin_order_field = 'comp_count'
    counter.short_description = _("Anzahl Components")

admin.site.register(Cluster, ClusterAdmin)

