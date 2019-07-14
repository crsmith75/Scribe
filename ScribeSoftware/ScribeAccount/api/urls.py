from django.urls import include, path
from rest_framework.routers import DefaultRouter
from ScribeAccount.api.views import ScribeAccountViewSet, AvatarUpdateView, ScribeCredentialsViewSet, TrackedTwitterAccountViewSet

router = DefaultRouter()
router.register(r"scribes", ScribeAccountViewSet)
router.register(r"credentials", ScribeCredentialsViewSet, basename="credentials")
router.register(r"trackedTwitterAccounts", TrackedTwitterAccountViewSet, basename="tracked-accounts")

urlpatterns = [
    path("", include(router.urls)),
    path("avatar/", AvatarUpdateView.as_view(), name="avatar-update")
]