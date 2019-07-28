from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from twitteraccounts.api.utils import createChain

from core.utils import generate_random_string
from twitteraccounts.models import twitterAccount

@receiver(pre_save, sender=twitterAccount)
def add_slug_to_question(sender, instance, *args, **kwargs):
    if instance and not instance.slug:
        slug = slugify(instance.handle)
        random_string = generate_random_string()
        instance.slug = slug + "-" + random_string

@receiver(pre_save, sender=twitterAccount)
def add_chainid(sender, instance, *args, **kwargs):
    if instance and not instance.chainid:
        chainid = createChain(instance.twitterid)
        instance.chainid = chainid

