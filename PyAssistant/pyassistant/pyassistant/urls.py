from django.contrib import admin
from django.urls import path, include
from . import views
from monitor import views as monitor_views

# Here I am defining URL routes for admin, main views, and app-specific routes
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('users/', include('users.urls')),
    path('processes/', include('monitor.urls')),
    path('storage/', include('storage.urls')),
    path('network/', include('network.urls')),

    # Here I am defining host-related routes for viewing, adding, and managing hosts
    path('hosts/', views.host_list, name='host_list'),
    path('add/', views.add_host, name='add_host'),
    path('hosts/<int:host_id>/processes/', views.view_host_processes, name='view_host_processes'),
    path('hosts/<int:host_id>/processes/kill/<int:pid>/', monitor_views.kill_process_view, name='kill_process'),
    path('hosts/<int:host_id>/install_vnc/', views.install_vnc, name='install_vnc'),
]
