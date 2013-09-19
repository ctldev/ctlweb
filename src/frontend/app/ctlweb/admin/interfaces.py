# vim: set fileencoding=utf-8
from django.contrib import admin
from django.db.models import Count

from ctlweb.models import Interfaces, Interfaces_Components
from ctlweb.admin.actions import delete_selected

from django.utils.translation import ugettext_lazy, ugettext as _

class Components_Inline(admin.StackedInline):
    model = Interfaces_Components
    extra = 0
    readonly_fields=('component',)

class InterfacesAdmin(admin.ModelAdmin):
    """
    Umfasst die Interfaceeinstellungen fürs Backend

    """
    fieldsets = (
        (None, {'fields': ('name',)}),
        (_('Code'), {'fields': ('ci',)}),
        (_('Hash'), {'fields': ('ci_hash',)}),
    )
    list_display = ['name', 'counter']
    search_fields = ('name',)
    ordering = ['name']
    readonly_fields = ('ci', 'name', 'ci_hash')
    inlines = [Components_Inline,]
    actions = [ delete_selected, ]

    def queryset(self, request):
        return Interfaces.objects.annotate(comp_count=Count('components'))

    def counter(self, obj):
        return obj.comp_count
    counter.admin_order_field = 'comp_count'
    counter.short_description = _("Anzahl Components")
admin.site.register(Interfaces, InterfacesAdmin)
