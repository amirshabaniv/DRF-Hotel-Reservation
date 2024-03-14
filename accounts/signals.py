from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from accounts.models import UserProfile

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def craete_user_information(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)