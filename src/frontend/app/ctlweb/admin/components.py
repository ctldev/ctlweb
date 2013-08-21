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
    extra = 0

class Cluster_Inline(admin.StackedInline):
    model = Components_Cluster
    extra = 0

class Programmer_Inline(admin.StackedInline):
    model = Programmer
    extra = 0

class ComponentsAdmin(admin.ModelAdmin):
    """
    Umfasst die Componenteinstellungen fürs Backend

    """
    fieldsets = (
        (None, {'fields': ('name', 'version', 'is_active')}),
        (_('Description'), {'fields': ('brief_description', 'description')}),
        (_('Dates'), {'fields': ('date', 'date_creation')}),
#        (_('Interfaces'), {'fields': ('interfaces',)}),
        )
    inlines = [Programmer_Inline, Interfaces_Inline, Cluster_Inline, ]
    list_display = ['name', 'version', 'is_active']
    search_fields = ('name', 
                     'version', 
                     'is_active', 
                     'homecluster')
    readonly_fields=('date', 'date_creation')
    actions = [ set_active,
                set_inactive ]

admin.site.register(Components, ComponentsAdmin)
