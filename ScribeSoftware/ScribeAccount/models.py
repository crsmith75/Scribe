from django.db import models
from django.contrib.auth.models import User

class ScribeAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.CharField(max_length=240)
    avatar = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class ScribeCredentials(models.Model):
    scribe_profile = models.OneToOneField(ScribeAccount, on_delete=models.CASCADE)
    twitterKey = models.CharField(max_length=240)
    twitterSecret = models.CharField(max_length=240)
    twitterAPIKey = models.CharField(max_length=240)
    twitterAPISecret = models.CharField(max_length=240)
    fctAddress = models.CharField(max_length=240)
    ecAddress = models.CharField(max_length=240)

    def __str__(self):
        return str(self.scribe_profile)

class TrackedTwitterAccount(models.Model):
    scribe_profile = models.ForeignKey(ScribeAccount, on_delete=models.CASCADE)
    twitter_handle = models.CharField(max_length = 100)
    twitter_id = models.IntegerField(unique=False)
    tracking_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{ self.twitter_handle } { self.twitter_id }"