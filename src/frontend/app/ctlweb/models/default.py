#vim: set fileencoding=utf-8
# vim: set fileencoding=utf-8
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
    user = models.OneToOneField(User, verbose_name=_("User"))
    key = models.TextField(_(u"Schlüssel"))
    class Meta:
        unique_together = ('user', 'key')
        app_label = 'ctlweb'
        verbose_name = _(u"Benutzerschlüssel")
        verbose_name_plural = _(u"Benutzerschlüssel")
	permissions = (
		("can_request_key", _(u"Darf sich einen Schlüssel anfordern")),
		("can_activate_user", _("Darf User freischalten")),
		("can_ban_user", _("Darf User bannen")))        

class Components(models.Model):
    name = models.CharField(_("Name"), max_length=100, unique="True")
    homeserver = models.ManyToManyField(Webserver, 
                                        verbose_name=_("Ursprungsserver"))
    homecluster = models.ManyToManyField(Cluster,
                                         through='Components_Cluster',
                                         verbose_name=_("Ursprungscluster"))
    programmer = models.EmailField(_("Programmierer"))
    brief_description = models.CharField(_("Kurzbeschreibung"), max_length=255)
    description = models.TextField(_("Beschreibung"))
    date = models.DateField(_("Datum"), auto_now_add=True)
    is_active = models.BooleanField(_("Freigeschaltet"))
    class Meta:
        app_label = 'ctlweb'
        verbose_name = _("Component")
        verbose_name_plural = _("Components")        
    permissions = (
		    ("can_see_description", _("Darf Beschreibungen lesen")),
		    ("can_see_homecluster", _("Darf die Ursprungscluster sehen")),
     		("can_see_homeserver", _("Darf die Ursprungsserver sehen")))

class Components_Cluster(models.Model):
    component = models.ForeignKey(Components)
    cluster = models.ForeignKey(Cluster)
    path = models.TextField(_("Pfad"))
    code = models.TextField(_("Implementierungscode"))
    class Meta:
        app_label = 'ctlweb'
    permissons = (
            ("can_see_path", _("Darf den Pfad sehen")),
            ("can_see_code", _("Darf den Implementierungscode sehen"))),

