from django.db import models

class Host(models.Model):
    hostname = models.CharField(max_length=255, unique=True)
    ip_address = models.GenericIPAddressField(unique=True)
    password = models.CharField(max_length=100, default='defaultpassword')
    
    def __str__(self):
        return f"{self.hostname} ({self.ip_address})"
