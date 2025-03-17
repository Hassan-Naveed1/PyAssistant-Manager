from django.urls import path
from .views import network_view

urlpatterns = [
    path('<int:host_id>/', network_view, name='network_view'),
]
