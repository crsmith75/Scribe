from django.db import models

# Create your models here.

class TrackedTwitterAccount(models.Model):
    twitter_handle = models.CharField(max_length = 100)
    twitter_id = models.IntegerField(unique=False)
    tracking_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{ self.twitter_handle } { self.twitter_id }"