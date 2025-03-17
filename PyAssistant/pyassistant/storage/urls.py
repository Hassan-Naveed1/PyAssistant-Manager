from django.urls import path
from .views import storage_view

urlpatterns = [
    path('<int:host_id>/', storage_view, name='storage_view'),
]
