from django.urls import path
from .views import process_list_view, kill_process

urlpatterns = [
    path('', process_list_view, name='process_list'),  # HTML Page
    path('kill/<int:pid>/', kill_process, name='kill_process'),  # Kill process API
]
