# vim : set fileencoding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ctlweb.models.components import *

class Interfaces(models.Model):
    """
    Repräsentiert die Interfaces

    """
    ci = models.TextField(_("Quellcode"))
    name = models.CharField(_("Name"), max_length=100)
    ci_hash = models.CharField(_("Hash"), max_length=2000, unique=True)
    components = models.ManyToManyField(Components,\
                                        verbose_name=_("Components"),\
                                        through='Interfaces_Components')

    class Meta:
        app_label = 'ctlweb'
        verbose_name = _("Interface")
        permissions = (
            ("can_see_key", "Can see the key"),
            ("can_see_ci", "Can see the ci"),)
    
    def __unicode__(self):
        return self.name

    def delete(self, *args, **kwargs):
        for comps in self.components.all(): 
            if len(comps.interfaces_set.exclude(pk=self.pk))==0:
                comps.delete()
        super(Interfaces, self).delete(*args, **kwargs)

class Interfaces_Components(models.Model):
    """
    Erstellt eine Verbindung zwischen Interfaces und Components.

    """
    interface = models.ForeignKey(Interfaces)
    component = models.ForeignKey(Components)
    class Meta:
        app_label = 'ctlweb'
        verbose_name = _("Interfaces - Components - Verbindung")
        verbose_name_plural = _("Interfaces - Components - Verbindungen")
    def __unicode__(self):
        return str(self.id)
