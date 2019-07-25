from django.db import models
from django.conf import settings

class twitterAccount(models.Model):
    twitter_handle = models.CharField(max_length = 100)
    twitter_id = models.IntegerField(unique=False)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                on_delete=models.CASCADE, 
                                related_name="account")

    def __str__(self):
        return f"{ self.twitter_handle } { self.twitter_id }"

class trackingInfo(models.Model):
    tracked_at = models.DateTimeField(auto_now_add=True)
    twitterAccount = models.ForeignKey(twitterAccount,
                                        on_delete=models.CASCADE, 
                                        related_name="trackingino")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                            on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


