from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from ctlweb.views import send_user, remove_user
from django.db.models.signals import post_save, post_delete
from ctlweb.models import Components, Components_Cluster

@receiver(post_save, sender=User)
def resend_user(sender, **kwargs):
    """
    Sends the saved User to all registered Clusters.
    """
    send_user(kwargs[u'instance'])

@receiver(post_delete, sender=User)
def redelete_user(sender, **kwargs):
    """
    Deletes the User from all registered Clusters.
    """
    remove_user(kwargs[u'instance'])

@receiver(post_save, sender=Components_Cluster)
@receiver(post_delete, sender=Components_Cluster)
def components_renamed(sender, **kwargs):
    """
    Create a new string for Components.name
    """
    comp = kwargs[u'instance'].component
    namelist = comp.components_cluster_set.\
            values_list('name', flat=True).distinct().order_by('name')
    comp.names = ', '.join(namelist)
    comp.save()
