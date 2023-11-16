from django.db.models.signals import post_save
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
            # updating the user if already created.
            profile = UserProfile.objects.get(user=instance)
            profile.save()
            print("user is updated")
        except:
            # Create the user if not exist
            UserProfile.objects.create(user=instance)
            print("user does not exits and I created one")
        

# @receiver(pre_save, sender=User)
# def pre_save_profile_receiver(sender, instance, **kwargs):
#     # print(instance.username, 'user is being created as we code')
#     pass
