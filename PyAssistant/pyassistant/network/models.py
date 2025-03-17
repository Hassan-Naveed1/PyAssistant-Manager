from django.db import models
from pyassistant.models import Host

class NetworkData(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    upload_speed = models.FloatField()  # Upload speed in KB/s or MB/s
    download_speed = models.FloatField()  # Download speed in KB/s or MB/s
    total_usage = models.FloatField()  # Total bandwidth used in MB/GB
    timestamp = models.DateTimeField(auto_now_add=True)  # Time of data collection

    def __str__(self):
        return f"{self.host.hostname} - {self.timestamp}"
