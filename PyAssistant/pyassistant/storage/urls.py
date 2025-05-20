from django.urls import path
from .views import storage_view

# Here I am defining the URL pattern to view storage details for a specific host
urlpatterns = [
    path('<int:host_id>/', storage_view, name='storage_view'),
]
