#vim: set fileencoding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Webserver(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    ip = models.IPAddressField(_("IP"), null="True")
    domain = models.CharField(_("Domain"), max_length=100 ,null="True")
    port = models.IntegerField(_("Port"), null="True")
    class Meta:
        unique_together = ('ip', 'domain')
        app_label = 'ctlweb'
        verbose_name = _("Webserver")
        verbose_name_plural = _("Webserver")

    def __unicode__(self):
        return self.name + u" (" + self.domain + u")"
