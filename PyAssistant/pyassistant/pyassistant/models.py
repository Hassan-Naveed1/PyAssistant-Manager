from django.db import models

class Host(models.Model):
    hostname = models.CharField(max_length=255, unique=True)
    ip_address = models.GenericIPAddressField(unique=True)
    username = models.CharField(max_length=100)  
    password = models.CharField(max_length=255)  

    def __str__(self):
        return self.hostname
