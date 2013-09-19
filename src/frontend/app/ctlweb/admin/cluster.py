# vim: set fileencoding=utf-8
from django.contrib import admin
from django.db.models import Count

from ctlweb.models import Cluster
from ctlweb.models import Components_Cluster
from ctlweb.admin.actions import delete_selected

from django.utils.translation import ugettext_lazy, ugettext as _

class Components_Inline(admin.StackedInline):
    model = Components_Cluster
    readonly_fields = ('name', 'component')
    extra = 0

class ClusterAdmin(admin.ModelAdmin):
    """
    Umfasst die Clustereinstellungen für das Backend

    """
    fieldsets = (
            (None, {'fields': ('hostname',)}),
            (_('Connection'), {'fields': ('port', 'username', 'key')}),
            )
    list_display = ['hostname', 'counter']
    search_fields = ('hostname',)
    ordering = ['hostname']
    inlines = [Components_Inline,]
    actions = [ delete_selected, ]
    
    def queryset(self, request):
        return Cluster.objects.annotate(comp_count=Count('components'))

    def counter(self, obj):
        return obj.comp_count
    counter.admin_order_field = 'comp_count'
    counter.short_description = _("Anzahl Components")

admin.site.register(Cluster, ClusterAdmin)

