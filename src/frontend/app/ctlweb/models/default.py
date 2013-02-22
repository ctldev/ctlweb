# vim: set fileencoding=utf-8
import datetime
from datetime import timedelta
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Webserver(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    ip = models.IPAddressField(_("IP"), null="True")
    domain = models.CharField(_("Domain"), max_length=100 ,null="True")
    port = models.IntegerField(_("Port"))
    class Meta:
        unique_together = ('ip', 'domain')
        app_label = 'ctlweb'
        verbose_name = _("Webserver")
        verbose_name_plural = _("Webserver")
                
class Cluster(models.Model):
    ip = models.IPAddressField(_("IP"), null="True")
    domain = models.CharField(_("Domain"), max_length=100, null="True")
    port = models.IntegerField(_("Port"))
    key = models.TextField(_(u"Schlüssel"), null="True")
    class Meta:
        unique_together = ('ip', 'domain')
        app_label = 'ctlweb'
        verbose_name = _("Cluster")
        verbose_name_plural = _("Cluster")
        
class Userkeys(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"))
    key = models.TextField(_(u"Schlüssel"))
    class Meta:
        unique_together = ('user', 'key')
        app_label = 'ctlweb'
        verbose_name = _(u"Benutzerschlüssel")
        verbose_name_plural = _(u"Benutzerschlüssel")
	permissions = (
		("can_request_key", u"Can request a userkey"),
		("can_activate_user", "Can activate a user"),
		("can_ban_user", "Can deactivate a user"))

    def set_active(self, User):
        if User.has_perm('can_activate_user'):
            self.user.is_active=True

    def set_inactive(self, User):
        if User.has_perm('can_ban_user'):
            self.user.is_active=False

class Components(models.Model):
    name = models.CharField(_("Name"), max_length=100, unique="True")
    homeserver = models.ManyToManyField(Webserver, 
                                        verbose_name=_("Ursprungsserver"))
    homecluster = models.ManyToManyField(Cluster,
                                         through='Components_Cluster',
                                         verbose_name=_("Ursprungscluster"))
    brief_description = models.CharField(_("Kurzbeschreibung"), max_length=255)
    description = models.TextField(_("Beschreibung"))
    date = models.DateTimeField(_("Datum"), auto_now=True)
    date_creation = models.DateTimeField(_("Erstellungsdatum"), auto_now_add=True)
    is_active = models.BooleanField(_("Freigeschaltet"))
    version = models.CharField(_("Versionsnummer"), max_length=10)
    class Meta:
        app_label = 'ctlweb'
        verbose_name = _("Component")
        verbose_name_plural = _("Components")        
    permissions = (
		    ("can_see_description", "Can read descriptions"),
		    ("can_see_homecluster", "Can see corresponding cluster"),
     		("can_see_homeserver", "Can see corresponding server"),
            ("can_set_active", "Can set active"))
    
    def set_active(self, User):
        if User.has_perm("can_set_active"):
            self.is_active=True

    def set_inactive(self, User):
        if User.has_perm("can_set_active"):
            self.is_active=False

    def save(self, user, *args, **kwargs):
        self.is_active = False
        self.programmer = user.email
        super(Components, self).save(*args, **kwargs)

class Interfaces(models.Model):
    name = models.CharField(_("Name"), max_length=100, unique="True")
    description = models.TextField(_("Beschreibung"))
    components = models.ManyToManyField(Components,
            verbose_name=_("Components"))
    key = models.CharField(_("Hash"), max_length=64, primary_key="True")
    class Meta:
        app_label = 'ctlweb'
        verbose_name = _("Interface")
    permissions = (
        ("can_see_key", "Can see the key."))

class Programmer(models.Model):
    component = models.ForeignKey(Components)
    email = models.EmailField(_("Programmierer"))
    class Meta:
        unique_together = ('component', 'email')
        app_label = 'ctlweb'

class Components_Cluster(models.Model):
    component = models.ForeignKey(Components)
    cluster = models.ForeignKey(Cluster)
    path = models.TextField(_("Pfad"))
    code = models.TextField(_("Implementierungscode"))
    class Meta:
        app_label = 'ctlweb'
    permissons = (
            ("can_see_path", "Can see filepath"),
            ("can_see_code", "Can see code to implement"))

class Mails(models.Model):
    text = models.TextField()
    class Meta:
        app_label = 'ctlweb'

class ModuleTokenValidation(models.Model):
    token = models.CharField(_("Token"), max_length=64)
    cluster = models.ForeignKey(Cluster)
    expiration_date = models.DateTimeField(_("Ablaufdatum"))
    class Meta:
        app_label = 'ctlweb'

    @staticmethod
    def create_token(token, cluster):
        date = datetime.datetime.today() + timedelta(days=2)
        to = ModuleTokenValidation(token=token, cluster=cluster,
                expiration_date=date)
        to.save()

    def is_valid(self, cluster):
        today = datetime.datetime.today()
        if isinstance(cluster, basestring):
            try:
                cluster = Cluster.objects.get(ip=cluster)
            except Cluster.DoesNotExist:
                return False
        if self.cluster == cluster:
            return (today <= self.date)
        return False
