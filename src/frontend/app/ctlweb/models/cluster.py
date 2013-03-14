# vim: set fileencoding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Cluster(models.Model):
    ip = models.IPAddressField(_("IP"), null="True")
    domain = models.CharField(_("Domain"), max_length=100, null="True")
    port = models.IntegerField(_("Port"), null="True")
    key = models.TextField(_(u"Schlüssel"), null="True")
    class Meta:
        unique_together = ('ip', 'domain')
        app_label = 'ctlweb'
        verbose_name = _("Cluster")
        verbose_name_plural = _("Cluster")
 
