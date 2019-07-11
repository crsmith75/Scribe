from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from ScribeAccount.models import ScribeAccount



# The Below function is in charge of making new profile instances
# The Receiver Decorator tells our fxn to expect a signal from User
# The post_save signal tells us that the signal will be sent as soon as the User is saved
# Hence, the Fxn will Know if it needs to create the profile or not

@receiver(post_save, sender=User)
def create_ScribeAccount(sender, instance, created, **kwargs):
#     print("Created: ", created)
    if created:
        ScribeAccount.objects.create(user=instance)