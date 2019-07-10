from django.urls import path
from AccountTracker.api.views import TrackedTwitterAccountDetailAPIView, TrackedTwitterAccountListCreateAPIView

urlpatterns = [
    path("accounts/", TrackedTwitterAccountListCreateAPIView.as_view(), name="account-list"),

    path("accounts/<int:pk>/", TrackedTwitterAccountDetailAPIView.as_view(), name="account-detail")
]