from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
#from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from ScribeAccount.models import ScribeAccount, ScribeCredentials
from ScribeAccount.api.serializers import ScribeAccountSerializer, ScribeAccountAvatarSerializer, ScribeCredentialsSerializer 
from ScribeAccount.api.permissions import IsOwnScribeAccountOrReadOnly, IsOwnerOrReadOnly

class AvatarUpdateView(generics.UpdateAPIView):
    serializer_class = ScribeAccountAvatarSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        scribe_object = self.request.user.scribeaccount
        return scribe_object


class ScribeAccountViewSet(mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):

    queryset = ScribeAccount.objects.all()
    serializer_class = ScribeAccountSerializer
    permission_classes = [IsAuthenticated, IsOwnScribeAccountOrReadOnly]
    
class ScribeCredentialsViewSet(ModelViewSet):
    queryset = ScribeCredentials.objects.all()
    serializer_class = ScribeCredentialsSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = ScribeCredentials.objects.all()
        username = self.request.query_params.get("username", None)
        if username is not None:
            queryset = queryset.filter(scribe_profile_user_username=username)
        return queryset

    #We override create function because we want to automatically connect status instance to the profile instance making it as soon as it is made
    def perform_create(self, serializer):
        scribe_profile = self.request.user.scribeaccount
        serializer.save(scribe_profile=scribe_profile)