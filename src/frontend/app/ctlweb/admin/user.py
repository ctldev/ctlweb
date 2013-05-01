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
        if User.objects.filter(is_superuser=True).count()>queryset.count():
            set_non_superuser(modeladmin, request, queryset)
            if User.objects.filter(is_staff=True).count()>queryset.count():
                set_non_staff(modeladmin, request, queryset)
                queryset.update(is_active=False)
        else :
            if User.objects.filter(is_staff=True).count()>queryset.count():
                set_non_staff(modeladmin, request, queryset)
                queryset.update(is_active=False)
            else :
                 queryset.filter(is_superuser=False, is_staff=False).update(is_active=False)
    set_inactive.short_description = _("Benutzer deaktivieren")
                          
def set_staff(modeladmin, request, queryset):
    queryset.update(is_staff=True, is_active=True)
    set_staff.short_description = _("Benutzer Redakteurrechte geben")

def set_non_staff(modeladmin, request, queryset):
    staff = User.objects.filter(is_staff=True).count()
    if staff > queryset.count():
        if User.objects.filter(is_superuser=True).count()>queryset.count():
            set_non_superuser(modeladmin, request, queryset)
        else :
            queryset.filter(is_superuser=False).update(is_staff=False)
    set_non_staff.short_description = _("Benutzer "+\
            "Redakteurrechte entziehen")

def set_superuser(modeladmin, request, queryset):
    if request.user.is_superuser:
        queryset.update(is_superuser=True, is_staff=True, is_active=True)
    set_superuser.short_description = _("Benutzer Adminrechte geben")

def set_non_superuser(modeladmin, request, queryset):
    if request.user.is_superuser:
        admins = User.objects.filter(is_superuser=True).count()
        if admins > queryset.count():
            queryset.update(is_superuser=False)
    set_non_superuser.short_description = _("Benutzer Adminrechte entziehen")

class CtlwebUserAdmin(UserAdmin):
    """
    Fügt dem Backend weitere Usereinstellungen hinzu

    """
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
                set_superuser,
                set_non_superuser,
              ]
    def save_model(self, request, obj, form, change):
        if obj == request.user :
            pass
        else :
            obj.save()

admin.site.unregister(User)
admin.site.register(User, CtlwebUserAdmin)
