from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
#from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from ScribeAccount.models import ScribeAccount
from ScribeAccount.api.serializers import ScribeAccountSerializer, ScribeAccountAvatarSerializer
from ScribeAccount.api.permissions import IsOwnScribeAccountOrReadOnly

class AvatarUpdateView(generics.UpdateAPIView):
    serializer_class = ScribeAccountAvatarSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile_object = self.request.user.profile
        return profile_object


class ScribeAccountViewSet(mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):

    queryset = ScribeAccount.objects.all()
    serializer_class = ScribeAccountSerializer
    permission_classes = [IsAuthenticated, IsOwnScribeAccountOrReadOnly]
    