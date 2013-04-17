# vim: set fileencoding=utf-8
import datetime
from datetime import timedelta
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ctlweb.models.webserver import *
from ctlweb.models.cluster import *

class Components(models.Model):
    """
    Repräsentiert die Components
    Stellt die Methoden set_active und set_inactive zur Verfügung.

    """
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
                ("can_set_active", "Can set active"),)
    
    def set_active(self, User):
        if User.has_perm("can_set_active"):
            self.is_active=True

    def set_inactive(self, User):
        if User.has_perm("can_set_active"):
            self.is_active=False

    def save(self, 
            #user, 
            *args, 
            **kwargs):
        self.is_active = False
        #self.programmer = user.email
        super(Components, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name + ' ' + self.version

class Components_Cluster(models.Model):
    """
    Erstellt die Verbindungsklasse zwischen den Components und den Clustern.
    Das code-Attribut stellt dabei den Quellcode der Component dar, während
    ctl den Befehl zur Ausführung speichert.

    """
    component = models.ForeignKey(Components)
    cluster = models.ForeignKey(Cluster)
    path = models.TextField(_("Pfad"))
    code = models.TextField(_("Quellcode"))
    ctl = models.TextField(_("CTL-Befehl"))  # Beim Speichern generiert
    class Meta:
        app_label = 'ctlweb'
        permissions = (
            ("can_see_path", "Can see filepath"),
            ("can_see_code", "Can see code to implement"),)
        verbose_name = _("Component - Cluster - Verbindung")
        verbose_name_plural = _("Component - Cluster - Verbindungen")

    def __create_ctl(self):
        """ return String
        Generiert den CTL-Befehl

        """
        #TODO
        return ""
    
    def save(self, *args, **kwargs):
        self.ctl = self.__create_ctl()
        super(Components_Cluster, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.id)
