from django.db import models
from pyassistant.models import Host  # Import Host model

class StorageData(models.Model):
    host = models.OneToOneField(Host, on_delete=models.CASCADE, related_name='storage')
    total_space = models.FloatField()
    used_space = models.FloatField()
    free_space = models.FloatField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Storage Data for {self.host.hostname}'
