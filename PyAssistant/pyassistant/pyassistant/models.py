# models.py in pyassistant app

from django.db import models

class Host(models.Model):
    # I store the hostname and IP address of the remote machine
    hostname = models.CharField(max_length=255, unique=True)
    ip_address = models.GenericIPAddressField(unique=True)
    username = models.CharField(max_length=100)  
    password = models.CharField(max_length=255)

    # I add a new field for the VNC port (default is 6080 for noVNC)
    vnc_port = models.PositiveIntegerField(default=6080)

    def __str__(self):
        return self.hostname

    # I create a method that returns the full VNC URL for this host
    def get_vnc_url(self):
        return f"http://{self.ip_address}:{self.vnc_port}"
