

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from App.models import *



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # Create a profile only when a new user is created (not on every save)
    if created:
        Profile.objects.create(user=instance)


