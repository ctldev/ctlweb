# vim: set fileencoding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
import datetime
from datetime import timedelta

from ctlweb.models.cluster import *

class Mails(models.Model):
    text = models.TextField()
    class Meta:
        app_label = 'ctlweb'

class ModuleTokenValidation(models.Model):
    """used for validation. remembers Tokens send to a Cluster and, when
    receiving a request, tests if the given token is (still) valid."""
    token = models.CharField(_("Token"), max_length=64)
    cluster = models.ForeignKey(Cluster)
    expiration_date = models.DateTimeField(_("Ablaufdatum"))
    class Meta:
        app_label = 'ctlweb'

    @staticmethod
    def create_token(token, cluster):
        """creating token with given timedelta with default of two days"""
        date = datetime.datetime.today() + timedelta(days=2)
        to = ModuleTokenValidation(token=token, cluster=cluster,
                expiration_date=date)
        to.save()

    def is_valid(self, cluster):
        """test if the given token is (still) valid"""
        today = datetime.datetime.today()
        if isinstance(cluster, basestring):
            try:
                cluster = Cluster.objects.get(ip=cluster)
            except Cluster.DoesNotExist:
                return False
        if self.cluster == cluster:
            return (today <= self.expiration_date)
        return False
