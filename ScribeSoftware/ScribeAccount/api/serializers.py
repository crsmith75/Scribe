from rest_framework import serializers
from ScribeAccount.models import ScribeAccount, ScribeCredentials, TrackedTwitterAccount
from .HelperFxns import createChain

class ScribeAccountSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)
    avatar = serializers.ImageField(read_only=True)

    class Meta:
        model = ScribeAccount
        fields = "__all__"

class ScribeAccountAvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScribeAccount
        fields = ("avatar")
    
class ScribeCredentialsSerializer(serializers.ModelSerializer):

    scribe_profile = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ScribeCredentials
        fields = "__all__"

class TrackedTwitterAccountSerializer(serializers.ModelSerializer):

    scribe_profile = serializers.StringRelatedField(read_only=True)
    chainID = serializers.SerializerMethodField()

    class Meta:
        model = TrackedTwitterAccount
        fields = "__all__"

    def get_chainID(self, object):
        twitter_id = object.twitter_id
        chain_id = createChain(twitter_id)
        return chain_id