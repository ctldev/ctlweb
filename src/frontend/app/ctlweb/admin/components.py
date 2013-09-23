# vim: set fileencoding=utf-8
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ctlweb.models import Components, \
                          Interfaces_Components, \
                          Components_Cluster, \
                          Programmer

def set_active(modeladmin, request, queryset):
    if request.user.has_perm('ctlweb.can_set_active'):
        queryset.update(is_active=True)
    set_active.short_description = _("Components aktivieren")

def set_inactive(modeladmin, request, queryset):
    if request.user.has_perm('ctlweb.can_set_active'):
        queryset.update(is_active=False)
    set_inactive.short_description = _("Components deaktiveren")

class Interfaces_Inline(admin.StackedInline):
    model = Interfaces_Components
    readonly_fields=('interface',)
    extra = 0
    max_num = 0
    can_delete = False

class Cluster_Inline(admin.StackedInline):
    model = Components_Cluster
    readonly_fields=('name', 'cluster')
    extra = 0
    max_num = 0
    can_delete = False

class Programmer_Inline(admin.StackedInline):
    model = Programmer
    readonly_fields=('email',)
    extra = 0
    can_delete = False
    max_num = 0


class ComponentsAdmin(admin.ModelAdmin):
    """
    Umfasst die Componenteinstellungen fürs Backend

    """
    fieldsets = (
        (None, {'fields': ('names', 'description', 'version', 'is_active',)}),
        (_('Dates'), {'fields': ('date', 'date_creation',)}),
        (_('Hash'), {'fields': ('exe_hash',)}),
        )
    inlines = [Programmer_Inline, Interfaces_Inline, Cluster_Inline, ]
    list_display = ['names',
                    'version', 
                    'is_active',
                    'date']
    ordering = ['names']
    search_fields = ('names',
                     'version', 
                     'is_active', 
                     'date')
    readonly_fields=('names', 'date', 'date_creation', 'version', 'exe_hash', 'description')
    actions = [ set_active,
                set_inactive ]
    def has_add_permission(self, request):
        return False


admin.site.register(Components, ComponentsAdmin)
