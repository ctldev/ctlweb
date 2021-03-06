from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from ctlweb.views.backend import send_user, remove_user
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
    Also, if a component is deleted on a cluster, check if component is reachable.
    Exterminate it otherwise.
    """
    try:
        comp = kwargs[u'instance'].component
        namelist = comp.components_cluster_set.\
                values_list('name', flat=True).distinct().order_by('name')
        comp.names = ', '.join(namelist)
        comp.save()
        connections = comp.components_cluster_set.all()
        if list(connections) == []:
            comp.delete()
    except Components.DoesNotExist:
        pass #do nothing, as component has already been deleted

@receiver(pre_save, sender=Components)
def components_active(sender, **kwargs):
    """
    Set is_active "False"
    """
    comp = kwargs[u'instance']
    if comp in Components.objects.all():
        comp2 = Components.objects.get(id=comp.id)
        if comp2.is_active :
            comp.is_active = False
    else :
        comp.is_active = False

