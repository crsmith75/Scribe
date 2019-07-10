from rest_framework import generics

from AccountTracker.api.serializers import TrackedTwitterAccountSerializer
from AccountTracker.models import TrackedTwitterAccount

class TrackedTwitterAccountListCreateAPIView(generics.ListCreateAPIView):

    queryset = TrackedTwitterAccount.objects.all()
    serializer_class = TrackedTwitterAccountSerializer
  

class TrackedTwitterAccountDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = TrackedTwitterAccount.objects.all()
    serializer_class = TrackedTwitterAccountSerializer
