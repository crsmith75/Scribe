from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from Account.models import Account



# The Below function is in charge of making new profile instances
# The Receiver Decorator tells our fxn to expect a signal from User
# The post_save signal tells us that the signal will be sent as soon as the User is saved
# Hence, the Fxn will Know if it needs to create the profile or not

@receiver(post_save, sender=User)
def create_Account(sender, instance, created, **kwargs):
#     print("Created: ", created)
    if created:
        Account.objects.create(user=instance)