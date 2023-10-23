from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile

@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
        print('User profile created')
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # Create the user if not exist
            UserProfile.objects.create(user=instance)
            print("user does not exits and I created one")
        print("user is updated")

@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    # print(instance.username, 'user is being created as we code')
    pass
