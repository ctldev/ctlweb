# vim: set fileencoding=utf-8
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from ctlweb.models import Userkeys
from ctlweb.models import UserMethods

def set_active(modeladmin, request, queryset):
    for q in queryset :
        q.is_active = True
        q.save(request)
    set_active.short_description = _("Benutzer aktivieren")
                   
def set_inactive(modeladmin, request, queryset):
    for q in queryset :
        q.is_active = False     
        q.save(request)
    set_inactive.short_description = _("Benutzer deaktivieren")
                          
def set_staff(modeladmin, request, queryset):
    for q in queryset :
        q.is_staff = True
        q.save(request)
    set_staff.short_description = _("Benutzer Redakteurrechte geben")

def set_non_staff(modeladmin, request, queryset):
    for q in queryset :
        q.is_staff = False
        q.save(request)
    set_non_staff.short_description = _("Benutzer "+\
            "Redakteurrechte entziehen")

def set_superuser(modeladmin, request, queryset):
    for q in queryset :
        q.is_superuser = True
        q.save(request)
    set_superuser.short_description = _("Benutzer Adminrechte geben")

def set_non_superuser(modeladmin, request, queryset):
    for q in queryset :
        q.is_superuser = False
        q.save(request)
    set_non_superuser.short_description = _("Benutzer Adminrechte entziehen")

class Key_Inline(admin.StackedInline):
    model = Userkeys
    extra = 0

class CtlwebUserAdmin(UserAdmin):
    """
    Fügt dem Backend weitere Usereinstellungen hinzu

    """
    readonly_fields=('last_login', 'date_joined')
    inlines = [Key_Inline, ]
    list_display = ['username', 
                    'first_name',
                    'last_name',  
                    'is_active', 
                    'is_staff', 
                    'is_superuser']
    actions = [ set_active, 
                set_inactive, 
                set_staff, 
                set_non_staff,
                set_superuser,
                set_non_superuser,
              ]
    def save_model(self, request, obj, form, change):
        print(obj)
        obj.save(request)

admin.site.unregister(User)
admin.site.register(User, CtlwebUserAdmin)
