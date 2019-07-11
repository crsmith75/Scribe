from django.db import models
from django.contrib.auth.models import User

class ScribeAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.CharField(max_length=240)
    avatar = models.ImageField(null=True, blank=True)
    twitterKey = models.CharField(max_length=240)
    twitterSecret = models.CharField(max_length=240)
    twitterAPIKey = models.CharField(max_length=240)
    twitterAPISecret = models.CharField(max_length=240)
    fctAddress = models.CharField(max_length=240)
    ecAddress = models.CharField(max_length=240)

    def __str__(self):
        return self.user.username

