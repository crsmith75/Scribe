from rest_framework import serializers
from twitteraccounts.models import twitterAccount


class twitterAccountSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    added_at = serializers.SerializerMethodField()
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = twitterAccount
        exclude = ["updated_at"]

    def get_added_at(self, instance):
        return instance.added_at.strftime("%B %d %Y")

    

    

