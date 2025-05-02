from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """This is a normal user who acts as an admin monitoring hosts."""
    is_admin = models.BooleanField(default=True)  # I am setting  All users as admins monitoring hosts
