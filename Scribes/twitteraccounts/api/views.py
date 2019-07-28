from rest_framework import generics, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from twitteraccounts.api.permissions import IsUserOrReadOnly
from twitteraccounts.api.serializers import twitterAccountSerializer
from twitteraccounts.models import twitterAccount

class twitterAccountViewSet(viewsets.ModelViewSet):
    queryset = twitterAccount.objects.all()
    serializer_class = twitterAccountSerializer
    permission_classes= [IsAuthenticated, IsUserOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class twitterAccountRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = twitterAccount.objects.all()
    serializer_class = twitterAccountSerializer
    permission_classes = [IsAuthenticated, IsUserOrReadOnly]
    
# class twitterAccountTrackAPIView(APIView):
#     serializer_class = twitterAccountSerializer
#     permission_classes = [IsAuthenticated, IsUserOrReadOnly]

#     def delete(self, request, pk):
#         twitteraccount = get_object_or_404(twitterAccount, pk=pk)
#         user = request.user

#         twitteraccount.trackers.remove(user)
#         twitteraccount.save()

#         serializer_context = {"request": request}
#         serializer = self.serializer_class(twitteraccount, context=serializer_context)

#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request, pk):
#         twitteraccount = get_object_or_404(twitterAccount, pk=pk)
#         twitteraccount = request.user

#         twitteraccount.trackers.add(user)
#         answer.save()

#         serializer_context = {"request": request}
#         serializer = self.serializer_class(twitteraccount, context=serializer_context)

#         return Response(serializer.data, status=status.HTTP_200_OK)