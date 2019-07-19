from rest_framework import serializers
from Account.models import Account, TwitterAccount

class AccountSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)
    avatar = serializers.ImageField(read_only=True)

    class Meta:
        model = Account
        fields = "__all__"

class AccountAvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ("avatar")

class TwitterAccountSerializer(serializers.ModelSerializer):

    user_account = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TwitterAccount
        fields = "__all__"