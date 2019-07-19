from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet

from Account.models import Account, TwitterAccount
from Account.api.serializers import AccountSerializer, AccountAvatarSerializer, TwitterAccountSerializer
from Account.api.permissions import IsOwnAccountOrReadOnly

class AvatarUpdateView(generics.UpdateAPIView):
    serializer_class = AccountAvatarSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        account_object = self.request.user.account
        return account_object


class AccountViewSet(mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, IsOwnAccountOrReadOnly]

class TwitterAccountViewSet(ModelViewSet):
    queryset = TwitterAccount.objects.all()
    serializer_class = TwitterAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = TwitterAccount.objects.all()
        username = self.request.query_params.get("username", None)
        if username is not None:
            queryset = queryset.filter(user_profile_user_username=username)
        return queryset

    #We override create function because we want to automatically connect status instance to the profile instance making it as soon as it is made
    def perform_create(self, serializer):
        user_account = self.request.user.account
        serializer.save(user_account=user_account)
