# vim : set fileencoding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ctlweb.models.components import *

class Interfaces(models.Model):
    """
    Repräsentiert die Interfaces

    """
    name = models.CharField(_("Name"), max_length=100, unique="True")
    description = models.TextField(_("Beschreibung"))
    components = models.ManyToManyField(Components,
                                        through='Interfaces_Components',
                                        verbose_name=_("Components"))
    key = models.CharField(_("Hash"), max_length=64, primary_key="True")
    class Meta:
        app_label = 'ctlweb'
        verbose_name = _("Interface")
        permissions = (
            ("can_see_key", "Can see the key"),)
    
    def __unicode__(self):
        return self.name

    def delete(self, *args, **kwargs):
        for comps in self.components:
            c_interfaces = comps.interfaces_set.all()
            c_interfaces = c_interfaces.exclude(id=self.id)
            if len(c_interfaces)==0:
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
