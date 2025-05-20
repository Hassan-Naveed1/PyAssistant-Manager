from django.db import models

# Here I am defining the Host model to store SSH and connection info for each remote machine
class Host(models.Model):
    hostname = models.CharField(max_length=255, unique=True)
    ip_address = models.GenericIPAddressField(unique=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)

    # Here I am adding a default VNC port field so each host can be accessed visually
    vnc_port = models.PositiveIntegerField(default=6080)

    def __str__(self):
        return self.hostname

    def get_vnc_url(self):
        return f"http://{self.ip_address}:{self.vnc_port}"
