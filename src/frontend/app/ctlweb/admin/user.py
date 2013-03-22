# vim: set fileencoding=utf-8
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from ctlweb.models import Userkeys

def set_active(modeladmin, request, queryset):
    queryset.update(is_active=True) 
    set_active.short_description = _("Benutzer aktivieren")
                   
def set_inactive(modeladmin, request, queryset):
    active = User.objects.filter(is_active=True).count()
    if active > queryset.count():
        set_non_staff(modeladmin, request, queryset)
        queryset.update(is_active=False)
    set_inactive.short_description = _("Benutzer deaktivieren")
                          
def set_staff(modeladmin, request, queryset):
    queryset.update(is_staff=True, is_active=True)
    set_staff.short_description = _("Benutzer Redakteurrechte geben")

def set_non_staff(modeladmin, request, queryset):
    staff = User.objects.filter(is_staff=True).count()
    if staff > queryset.count():
        set_non_admin(modeladmin, request, queryset)
        queryset.update(is_staff=False)
    set_non_staff.short_description = _("Benutzer "+\
            "Redakteurrechte entziehen")

def set_admin(modeladmin, request, queryset):
    if request.user.is_superuser:
        queryset.update(is_superuser=True, is_staff=True, is_active=True)
    set_admin.short_description = _("Benutzer Adminrechte geben")

def set_non_admin(modeladmin, request, queryset):
    if request.user.is_superuser:
        admins = User.objects.filter(is_superuser=True).count()
        if admins > queryset.count():
            queryset.update(is_superuser=False)
    set_non_admin.short_description = _("Benutzer Adminrechte entziehen")

class CtlwebUserAdmin(UserAdmin):
    readonly_fields=('last_login', 'date_joined')
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
                set_admin,
                set_non_admin,
              ]

admin.site.unregister(User)
admin.site.register(User, CtlwebUserAdmin)
