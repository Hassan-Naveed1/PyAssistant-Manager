from django.db import models
from pyassistant.models import Host  # I am linking messages to a host

class Message(models.Model):
    # Every message belongs to a specific host
    host = models.ForeignKey(Host, on_delete=models.CASCADE)  
    sender = models.CharField(max_length=50)  # Sender could be "Server" or "Host"
    content = models.TextField()  # Message content
    timestamp = models.DateTimeField(auto_now_add=True)  # Auto set time when message is created

    def __str__(self):
        return f"{self.sender} to {self.host.hostname}: {self.content[:30]}"
