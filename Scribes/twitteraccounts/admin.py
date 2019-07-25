from django.contrib import admin

from twitteraccounts.models import trackingInfo, twitterAccount 

admin.site.register(trackingInfo)
admin.site.register(twitterAccount)