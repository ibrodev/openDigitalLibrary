from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile

@receiver(post_save, sender=User)
def create_author_profile(sender, instance, created, **kwargs):
    if created and (instance.user_type == "USER" or instance.user_type == "ADMIN"):
        Profile.objects.create(account=instance)
        

