from django.urls import include, path
from rest_framework.routers import DefaultRouter
from Account.api.views import AccountViewSet, AvatarUpdateView

router = DefaultRouter()
router.register(r"accounts", AccountViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("avatar/", AvatarUpdateView.as_view(), name="avatar-update")
]