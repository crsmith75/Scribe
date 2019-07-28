from django.urls import path
from users.api.views import CurrentUserAPIView

#current-user will be an endpoint corresponding to the username of the authenticated user
urlpatterns = [
    path("user/", CurrentUserAPIView.as_view(), name="current-user")
]