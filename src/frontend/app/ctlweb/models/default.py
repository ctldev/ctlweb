# vim: set fileencoding=utf-8
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

class webserver(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    ip = models.IPAddressField(_("IP"), null="True")
    domain = models.CharField(_("Domain"), max_length=100 ,null="True")
    port = models.IntegerField(_("Port"))
    class Meta:
        unique_together = ('ip', 'domain')
        app_label = 'ctlweb'
        verbose_name = _("Webserver")
        verbose_name_plural = _("Webserver")
                
class cluster(models.Model):
    ip = models.IPAddressField(_("IP"), null="True")
    domain = models.CharField(_("Domain"), max_length=100, null="True")
    port = models.IntegerField(_("Port"))
    key = models.TextField(_(u"Schlüssel"), null="True")
    class Meta:
        unique_together = ('ip', 'domain')
        app_label = 'ctlweb'
        verbose_name = _("Cluster")
        verbose_name_plural = _("Cluster")
        
class userkeys(models.Model):
    user = models.OneToOneField(User, verbose_name=_("User"))
    key = models.TextField(_(u"Schlüssel"))
    class Meta:
        unique_together = ('user', 'key')
        app_label = 'ctlweb'
        verbose_name = _(u"Benutzerschlüssel")
        verbose_name_plural = _(u"Benutzerschlüssel")
        
class components(models.Model):
    name = models.CharField(_("Name"), max_length=100, unique="True")
    path = models.TextField(_("Pfad"))
    homeserver = models.ManyToManyField(webserver, 
                                        verbose_name=_("Ursprungsserver"))
    homecluster = models.ManyToManyField(cluster,
                                         verbose_name=_("Ursprungscluster"))
    programmer = models.EmailField(_("Programmierer"))
    brief_description = models.CharField(_("Kurzbeschreibung"), max_length=255)
    description = models.TextField(_("Beschreibung"))
    date = models.DateField(_("Datum"), auto_now_add=True)
    is_active = models.BooleanField(_("Freigeschaltet"))
    code = models.TextField(_("Implementierungscode"))
    class Meta:
        app_label = 'ctlweb'
        verbose_name = _("Component")
        verbose_name_plural = _("Components")        
