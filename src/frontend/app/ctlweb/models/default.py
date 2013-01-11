from django.contrib.auth.models import User
from django.db import models

class webserver(models.Model):
    ip = models.IPAddressField(null="True")
    domain = models.CharField(max_length=100 ,null="True")
    port = models.IntegerField()
    class Meta:
        unique_together = ('ip', 'domain')
        app_label = 'ctlweb'
        
class cluster(models.Model):
    ip = models.IPAddressField(null="True")
    domain = models.CharField(max_length=100, null="True")
    port = models.IntegerField()
    key = models.TextField(null="True")
    class Meta:
        unique_together = ('ip', 'domain')
        app_label = 'ctlweb'
        
class userkeys(models.Model):
    user = models.OneToOneField(User)
    key = models.TextField()
    class Meta:
        unique_together = ('user', 'key')
        app_label = 'ctlweb'
        
class components(models.Model):
    name = models.CharField(max_length=100, unique="True")
    pfad = models.TextField()
    homeserver = models.ManyToManyField(webserver)
    homecluster = models.ManyToManyField(cluster)
    programmer = models.EmailField()
    discription = models.TextField()
    class Meta:
        app_label = 'ctlweb'
