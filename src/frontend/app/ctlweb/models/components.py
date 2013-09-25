# vim: set fileencoding=utf-8
import datetime
from datetime import timedelta
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ctlweb.models.cluster import *

class Components(models.Model):
    """
    Repräsentiert die Components
    Stellt die Methoden set_active und set_inactive zur Verfügung.

    """
    names = models.TextField(_("Namen"), blank=True, null=True)
    description = models.TextField(_("Beschreibung"))
    date = models.DateTimeField(_(u"Zuletzt geändert am"), auto_now=True)
    date_creation = models.DateTimeField(_("Erstellungsdatum"),\
                                         auto_now_add=True)
    is_active = models.BooleanField(_("Freigeschaltet"))
    version = models.CharField(_("Version"), max_length=255)
    exe_hash = models.CharField(_("Hash"), max_length=2000, unique=True)
    homecluster = models.ManyToManyField(Cluster,\
                                         verbose_name=_("Ursprungscluster"),\
                                         through='Components_Cluster')
    class Meta:
        app_label = 'ctlweb'
        verbose_name = _("Component")
        verbose_name_plural = _("Components")        
        permissions = (
		        ("can_see_description", "Can read descriptions"),
		        ("can_see_homecluster", "Can see corresponding cluster"),
                ("can_set_active", "Can set active"),)
    
    def set_active(self, User):
        if User.has_perm("can_set_active"):
            self.is_active=True

    def set_inactive(self, User):
        if User.has_perm("can_set_active"):
            self.is_active=False

    @property
    def brief_description(self):
        if '.' in self.description:
            descriptionparts = self.description.split(". ")
            short_description = descriptionparts[0] + ". "
        else:
            short_description = self.description[:255]
        return short_description

    def __unicode__(self):
        return self.names

class Components_Cluster(models.Model):
    """
    Erstellt die Verbindungsklasse zwischen den Components und den Clustern.
    Das code-Attribut stellt dabei den Quellcode der Component dar, während
    ctl den Befehl zur Ausführung speichert.

    """
    component = models.ForeignKey(Components)
    cluster = models.ForeignKey(Cluster)
    name = models.CharField(_("Name"), max_length=100)

    class Meta:
        unique_together = ('cluster', 'name')
        app_label = 'ctlweb'
        verbose_name = _("Component - Cluster - Verbindung")
        verbose_name_plural = _("Component - Cluster - Verbindungen")

    def __unicode__(self):
        return str(self.id)


class Programmer(models.Model):
    """
    Repräsentiert die Programmierer

    """
    component = models.ForeignKey(Components)
    email = models.EmailField(_("Programmierer"))
    class Meta:
       verbose_name = _("Programmierer")
       verbose_name_plural = _("Programmierer")
       unique_together = ('component', 'email')
       app_label = 'ctlweb'

    def __unicode__(self):
        return self.email
