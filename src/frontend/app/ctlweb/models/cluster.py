# vim: set fileencoding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Cluster(models.Model):
    """
    Repräsentiert die Cluster

    """
    ip = models.IPAddressField(_("IP"), blank=True, null=True)
    domain = models.CharField(_("Domain"), max_length=100, blank=True, null=True)
    username = models.CharField(_("Benutzer"), max_length=100, blank=True, null=True)
    port = models.IntegerField(_("Port"), blank=True, null=True)
    key = models.TextField(_(u"Schlüssel"), blank=True, null=True)
    class Meta:
        unique_together = ('ip', 'domain')
        app_label = 'ctlweb'
        verbose_name = _("Cluster")
        verbose_name_plural = _("Cluster")
        permissions = (
                ("can_see_ssh_data", 
                    "Can see port and username required for SSH"),)

    def delete(self, *args, **kwargs):
        for comps in self.components_set.all():
            print(comps.homecluster)
            if len(comps.homecluster.exclude(id=self.id))==0:
                comps.delete()
        super(Cluster, self).delete(*args, **kwargs)

    def __unicode__(self):
        return self.domain
