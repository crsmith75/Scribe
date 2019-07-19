from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet

from Account.models import Account
from Account.api.serializers import AccountSerializer, AccountAvatarSerializer
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