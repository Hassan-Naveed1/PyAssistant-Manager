from django.urls import path
from .views import host_processes_view, kill_process_view 

urlpatterns = [
    path('hosts/<int:host_id>/processes/', host_processes_view, name='host_processes'),
    path('hosts/<int:host_id>/processes/kill/<int:pid>/', kill_process_view, name='kill_process'),  # ✅ Correct function name
]
