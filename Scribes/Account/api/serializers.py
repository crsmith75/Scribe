from rest_framework import serializers
from Account.models import Account

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