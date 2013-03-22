# vim: set fileencoding=utf-8
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Userkeys(models.Model):
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
        
    def set_active(self, User):
        if User.has_perm('can_activate_user'):
            self.user.is_active=True

    def set_inactive(self, User):
        if User.has_perm('can_ban_user'):
            self.user.is_active=False

    def __unicode__(self):
        return self.key
