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

class Cluster_Inline(admin.StackedInline):
    model = Components_Cluster
    readonly_fields=('name', 'cluster')
    extra = 0

class Programmer_Inline(admin.StackedInline):
    model = Programmer
    readonly_fields=('email',)
    extra = 0


class ComponentsAdmin(admin.ModelAdmin):
    """
    Umfasst die Componenteinstellungen fürs Backend

    """
    fieldsets = (
        (None, {'fields': ('description', 'version', 'is_active',)}),
        (_('Dates'), {'fields': ('date', 'date_creation',)}),
        (_('Hash'), {'fields': ('exe_hash',)}),
        )
    inlines = [Programmer_Inline, Interfaces_Inline, Cluster_Inline, ]
    list_display = ['names',
                    'version', 
                    'is_active',
                    'date']
    ordering = ['components_cluster__name']
    search_fields = ('components_cluster__name',
                     'version', 
                     'is_active', 
                     'date')
    readonly_fields=('date', 'date_creation', 'version', 'exe_hash', 'description')
    actions = [ set_active,
                set_inactive ]


    def names(self, obj):
        namelist = obj.components_cluster_set.values_list('name',
                flat=True).order_by('name').distinct()
        namestring = ', '.join(namelist)
        return namestring
    names.admin_order_field = 'components_cluster__name'
    names.short_description =_("Namen")

    def queryset(self,request):
        qs = super(ComponentsAdmin, self).queryset(request)
        ids = qs.values('pk')
        qs = Components.objects.filter(pk__in=ids).distinct()
        return qs

admin.site.register(Components, ComponentsAdmin)
