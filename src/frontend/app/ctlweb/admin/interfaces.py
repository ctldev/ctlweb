# vim: set fileencoding=utf-8
from django.contrib import admin
from django.db.models import Count

from ctlweb.models import Interfaces, Interfaces_Components
from ctlweb.admin.actions import delete_selected

from django.utils.translation import ugettext_lazy, ugettext as _

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
    list_display = ['name', 'key', 'counter']
    search_fields = ('key', 'name', 'description')
    ordering = ['key']
    inlines = [Components_Inline,]
    actions = [ delete_selected, ]

    def queryset(self, request):
        return Interfaces.objects.annotate(comp_count=Count('components'))

    def counter(self, obj):
        return obj.comp_count
    counter.admin_order_field = 'comp_count'
    counter.short_description = _("Anzahl Components")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request):
        return False
admin.site.register(Interfaces, InterfacesAdmin)
