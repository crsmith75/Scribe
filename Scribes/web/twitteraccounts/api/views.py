from rest_framework import generics, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from kafka import SimpleProducer, KafkaClient, KafkaConsumer

from twitteraccounts.api.permissions import IsUserOrReadOnly
from twitteraccounts.api.serializers import twitterAccountSerializer
from twitteraccounts.models import twitterAccount

class twitterAccountViewSet(viewsets.ModelViewSet):
    queryset = twitterAccount.objects.all()
    serializer_class = twitterAccountSerializer
    permission_classes= [IsAuthenticated, IsUserOrReadOnly]

    def perform_create(self, serializer):
        twitteraccount = serializer.save(user=self.request.user)
        
class twitterAccountRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = twitterAccount.objects.all()
    serializer_class = twitterAccountSerializer
    permission_classes = [IsAuthenticated, IsUserOrReadOnly]
    
