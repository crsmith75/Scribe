from django.contrib.auth.models import AbstractUser

# Remove Pass and define the specific fields needed for custom user
class CustomUser(AbstractUser):
    pass
