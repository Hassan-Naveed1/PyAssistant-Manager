from django import forms
from .models import Host
# Here I am creating a form to handle host creation and input validation
class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = ['hostname', 'ip_address', 'username', 'password', 'email']  
