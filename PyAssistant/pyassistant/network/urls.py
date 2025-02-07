from django.urls import path
from . import views

urlpatterns = [
    path('', views.network_usage, name='network_usage'),  # Main page at /network/
    path('api/data/', views.get_network_usage_data, name='network_api_data'),  # API at /network/api/data/
]
