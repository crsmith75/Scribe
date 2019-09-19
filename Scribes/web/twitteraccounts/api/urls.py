from django.urls import include, path 
from rest_framework.routers import DefaultRouter

from twitteraccounts.api import views as qv

router = DefaultRouter()
router.register(r"twitteraccounts", qv.twitterAccountViewSet)

urlpatterns = [
    path("", include(router.urls)),

    path("twitteraccounts/<int:pk>/",
          qv.twitterAccountRUDAPIView.as_view(),
          name="account-detail"),
]