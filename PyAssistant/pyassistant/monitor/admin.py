from django.contrib import admin
from .models import ProcessMonitor

@admin.register(ProcessMonitor)
class ProcessMonitorAdmin(admin.ModelAdmin):
    list_display = ('name', 'pid', 'execution_time', 'cpu_usage', 'network_usage', 'created_at')
    search_fields = ('name', 'pid')
