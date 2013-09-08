# vim: set fileencoding=utf-8
from django.contrib import admin
from django.db.models import Count

from ctlweb.models import Interfaces, Interfaces_Components

from django import template
from django.core.exceptions import PermissionDenied
from django.contrib.admin import helpers
from django.contrib.admin.util import get_deleted_objects, model_ngettext
from django.db import router
from django.shortcuts import render_to_response
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy, ugettext as _

class Components_Inline(admin.StackedInline):
    model = Interfaces_Components
    extra = 0

def delete_selected(modeladmin, request, queryset):
    """
    Default action which deletes the selected objects.

    This action first displays a confirmation page whichs shows all the
    deleteable objects, or, if the user has no permission one of the related
    childs (foreignkeys), a "permission denied" message.

    Next, it delets all selected objects and redirects back to the change list.

    Copy: django/contrib/admin/action.py
    """
    opts = modeladmin.model._meta
    app_label = opts.app_label

    if not modeladmin.has_delete_permission(request):
        raise PermissionDenied

    using = router.db_for_write(modeladmin.model)

    deletable_objects, perms_needed, protected = get_deleted_objects(
        queryset, opts, request.user, modeladmin.admin_site, using)

    if request.POST.get('post'):
        if perms_needed:
            raise PermissionDenied
        n = queryset.count()
        if n:
            for obj in queryset:
                obj_display = force_unicode(obj)
                obj.delete()
                modeladmin.log_deletion(request, obj, obj_display)
            modeladmin.message_user(request, _("Successfully deleted %(count)d %(items)s.") % {
                "count": n, "items": model_ngettext(modeladmin.opts, n)
            })
        return None

    if len(queryset) == 1:
        objects_name = force_unicode(opts.verbose_name)
    else:
        objects_name = force_unicode(opts.verbose_name_plural)

    if perms_needed or protected:
        title = _("Cannot delete %(name)s") % {"name": objects_name}
    else:
        title = _("Are you sure?")

    context = {
        "title": title,
        "objects_name": objects_name,
        "deletable_objects": [deletable_objects],
        'queryset': queryset,
        "perms_lacking": perms_needed,
        "protected": protected,
        "opts": opts,
        "root_path": modeladmin.admin_site.root_path,
        "app_label": app_label,
        'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
    }

    return render_to_response(modeladmin.delete_selected_confirmation_template or [
        "admin/%s/%s/delete_selected_confirmation.html" % (app_label, opts.object_name.lower()),
        "admin/%s/delete_selected_confirmation.html" % app_label,
        "admin/delete_selected_confirmation.html"
    ], context, context_instance=template.RequestContext(request))

delete_selected.short_description = ugettext_lazy("Delete selected %(verbose_name_plural)s")

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
admin.site.register(Interfaces, InterfacesAdmin)
