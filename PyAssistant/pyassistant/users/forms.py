from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

# Here I am creating a custom user registration form for admins monitoring hosts
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "password1", "password2"]
