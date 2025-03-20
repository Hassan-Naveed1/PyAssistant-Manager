"""
URL configuration for pyassistant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from monitor import views as monitor_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('processes/', include('monitor.urls')),
    path('storage/', include('storage.urls')),
    path('network/', include('network.urls')),
    path('chat/', include('message.urls')),


    # Host-related URLs
    path('hosts/', views.host_list, name='host_list'),
    path('add/', views.add_host, name='add_host'),
    path('hosts/<int:host_id>/processes/', views.view_host_processes, name='view_host_processes'),
    path('hosts/<int:host_id>/processes/kill/<int:pid>/', monitor_views.kill_process_view, name='kill_process'),
]


