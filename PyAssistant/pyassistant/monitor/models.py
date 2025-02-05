from django.db import models
import psutil
import datetime

class ProcessMonitor(models.Model):
    name = models.CharField(max_length=255)  
    pid = models.IntegerField(unique=True)  
    execution_time = models.DurationField()  
    cpu_usage = models.FloatField() 
    network_usage = models.FloatField()  

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (PID: {self.pid})"
