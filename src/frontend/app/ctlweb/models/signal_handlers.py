from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from ctlweb.views import send_user, remove_user

@receiver("post_save", sender=User)
def resend_user(sender, **kwargs):
    """
    Sends the saved User to all registered Clusters.
    """
    send_user(kwargs[u'instance'])

@receiver("post_delete", sender=User)
def redelete_user(sender, **kwargs):
    """
    Deletes the User from all registered Clusters.
    """
    remove_user(kwargs[u'instance'])
