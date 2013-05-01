# vim: set fileencoding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ctlweb.models.components import *

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
