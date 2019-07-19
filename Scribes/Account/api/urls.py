from django.urls import include, path
from rest_framework.routers import DefaultRouter
from Account.api.views import AccountViewSet, AvatarUpdateView, TwitterAccountViewSet

router = DefaultRouter()
router.register(r"accounts", AccountViewSet)
router.register(r"twitteraccounts", TwitterAccountViewSet, basename="tracked-accounts")

urlpatterns = [
    path("", include(router.urls)),
    path("avatar/", AvatarUpdateView.as_view(), name="avatar-update")
]