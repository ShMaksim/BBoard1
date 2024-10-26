from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from .utils import send_registration_confirmation

@receiver(post_save, sender=User)
def create_registration_code(sender, instance, created, **kwargs):
    if created:
        instance.registration_code = get_random_string(length=32)
        instance.is_active = False
        instance.save()
        send_registration_confirmation(instance)