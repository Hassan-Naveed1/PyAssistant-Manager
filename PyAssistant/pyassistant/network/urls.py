from django.urls import path
from .views import network_view

# Here I am defining the URL pattern for viewing network usage of a specific host
urlpatterns = [
    path('<int:host_id>/', network_view, name='network_view'),
]
