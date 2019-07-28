from rest_framework import serializers
from twitteraccounts.models import twitterAccount

class twitterAccountSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    added_at = serializers.SerializerMethodField()
    # tracking_count = serializers.SerializerMethodField()
    # user_has_tracked = serializers.SerializerMethodField()
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = twitterAccount
        exclude = ["updated_at"]

    def get_added_at(self, instance):
        return instance.added_at.strftime("%B %d %Y")

    # def get_tracking_count(self, instance):
    #     return instance.trackers.count()

    # def get_user_has_tracked(self, instance):
    #     request = self.context.get("request")
    #     return instance.trackers.filter(pk=request.user.pk).exists()

    

    

