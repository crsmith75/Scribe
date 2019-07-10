from rest_framework import serializers
from AccountTracker.models import TrackedTwitterAccount
from .HelperFxns import createChain

class TrackedTwitterAccountSerializer(serializers.ModelSerializer):

    chainID = serializers.SerializerMethodField()

    class Meta:
        model = TrackedTwitterAccount
        fields = "__all__"

    def get_chainID(self, object):
        twitter_id = object.twitter_id
        chain_id = createChain(twitter_id)
        return chain_id