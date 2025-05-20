from django.urls import path
from .views import register, login_view, logout_view


# Here I am defining authentication routes for user registration, login, and logout
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
