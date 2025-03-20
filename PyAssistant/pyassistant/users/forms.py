from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """Custom form for registering normal users as admins monitoring hosts."""
    
    class Meta:
        model = CustomUser
        fields = ["username", "password1", "password2"]
