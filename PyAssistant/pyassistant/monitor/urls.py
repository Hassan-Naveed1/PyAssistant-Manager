from django.urls import path
from . import views
from pyassistant.views import add_host, host_list
from pyassistant.views import add_host, host_list

urlpatterns = [
    path('', views.process_list_view, name='process_list'),
    path('kill/<int:pid>/', views.kill_process, name='kill_process'),
    path('hosts/<int:host_id>/processes/kill/<int:pid>/', views.kill_process, name='kill_process'),

    
]
