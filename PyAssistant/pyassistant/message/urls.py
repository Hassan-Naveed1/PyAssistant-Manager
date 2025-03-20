from django.urls import path
from .views import send_message_page, send_message, get_messages

urlpatterns = [
    path('hosts/<int:host_id>/chat/', send_message_page, name='send_message_page'),  # ✅ Route for chat page
    path('hosts/<int:host_id>/chat/send/', send_message, name='send_message'),
    path('hosts/<int:host_id>/chat/messages/', get_messages, name='get_messages'),
]
