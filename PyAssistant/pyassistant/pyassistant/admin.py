from django.contrib import admin
from .models import Host

@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'ip_address')
