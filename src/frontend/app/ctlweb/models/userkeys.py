# vim: set fileencoding=utf-8
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Userkeys(models.Model):
    """
    Repräsentiert die Userkeys
    Stellt Methoden zur Verfügung um User zu blocken (set_inactive)
    bzw. wieder zu aktivieren (set_active).

    """
    user = models.ForeignKey(User, verbose_name=_("User"))
    key = models.TextField(_(u"Schlüssel"))
    class Meta:
        permissions = (
		    ("can_request_key", "Can request a userkey"),
		    ("can_activate_user", "Can activate a user"),
		    ("can_ban_user", "Can deactivate a user"),)
        unique_together = ('user', 'key')
        app_label = 'ctlweb'
        verbose_name = _(u"Benutzerschlüssel")
        verbose_name_plural = _(u"Benutzerschlüssel")
        
#    def set_active(self, User):
#        if User.has_perm('can_activate_user'):
#            self.user.is_active=True
#
#    def set_inactive(self, User):
#        if User.has_perm('can_ban_user'):
#            self.user.is_active=False

    def __unicode__(self):
        return self.key

class UserMethods(User):
    def save(self, request=None, *args, **kwargs):
        v_user = request.user        
        if request == None :
           super(User, self).save(*args, **kwargs)
        try :
            user = User.objects.get(id=self.id)
            if v_user.id == self.id :
                # Änderungen der eigenen Informationen
                if (self.is_active == user.is_active) and \
                    (self.is_staff == user.is_staff) and \
                    (self.is_superuser == user.is_superuser) :
                    super(User, self).save(*args,**kwargs)
            else : # Änderung von fremden Daten
                #active-staff-superuser
                acstsu = User.objects.filter(is_active=True, 
                                             is_staff=True,
                                             is_superuser=True)
                if acstsu.count() > 1 :
                    super(User, self).save(*args, **kwargs)
                else :
                    if acstsu.filter(id = self.id).count() == 0 :
                        super(User, self).save(*args, **kwargs)

                    #Hinzufügen von Status
            if not user.is_superuser and self.is_superuser :
                self.is_active = True
                self.is_staff = True
                super(User, self).save(*args, **kwargs)
            elif not user.is_staff and self.is_staff :
                self.is_active = True
                super(User, self).save(*args, **kwargs)
            elif not user.is_active and self.is_active :
                super(User, self).save(*args, **kwargs)
        except :
            super(User, self).save(*args, **kwargs)

    class Meta:
        proxy=True
        app_label = 'auth'
        verbose_name = _("User")
        verbose_name_plural = _("User")
