# vim: set fileencoding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Cluster(models.Model):
    """
    Repräsentiert die Cluster

    """
    hostname = models.CharField(_("Host/IP"), max_length=255, unique=True)
    username = models.CharField(_("Benutzer"), max_length=100)
    port = models.IntegerField(_("Port"))
    key = models.FilePathField(_(u"Schlüssel"), null=True, blank=True)

    class Meta:
        app_label = 'ctlweb'
        verbose_name = _("Cluster")
        verbose_name_plural = _("Cluster")
        permissions = (
                ("can_see_ssh_data", 
                    "Can see port and username required for SSH"),)

    def delete(self, *args, **kwargs):
        for comps in self.components_set.all():
            if len(comps.homecluster.exclude(id=self.id))==0:
                comps.delete()
        super(Cluster, self).delete(*args, **kwargs)

    def __unicode__(self):
        return self.hostname
