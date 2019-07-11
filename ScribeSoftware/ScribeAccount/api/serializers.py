from rest_framework import serializers
from ScribeAccount.models import ScribeAccount

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