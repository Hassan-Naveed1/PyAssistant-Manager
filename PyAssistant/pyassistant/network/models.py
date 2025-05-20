from django.db import models
from pyassistant.models import Host

# Here I am defining the model to store network usage data for each host
class NetworkData(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    upload_speed = models.FloatField()
    download_speed = models.FloatField()
    total_usage = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.host.hostname} - {self.timestamp}"
