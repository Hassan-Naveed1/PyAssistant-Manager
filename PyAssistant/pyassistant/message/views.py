from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pyassistant.models import Host
from .models import Message
import json

@csrf_exempt  # ✅ Allowing POST requests without CSRF for now
def send_message(request, host_id):
    """Handles sending a message from the server to a host."""
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)

    try:
        data = json.loads(request.body)  # ✅ Parsing JSON request
        host = get_object_or_404(Host, id=host_id)

        # Now, I will create a new message
        message = Message.objects.create(
            host=host,
            sender="Server",
            content=data.get("content")
        )

        return JsonResponse({"success": True, "message": "Message sent successfully."})

    except Exception as e:
        return JsonResponse({"success": False, "message": f"Error: {str(e)}"}, status=500)

def get_messages(request, host_id):
    # Now, I will fetch all messages related to a specific host
    messages = Message.objects.filter(host_id=host_id).order_by("timestamp")

    # I will return the messages as a JSON response
    return JsonResponse({"messages": list(messages.values("sender", "content", "timestamp"))})


from django.shortcuts import render, get_object_or_404
from pyassistant.models import Host

def send_message_page(request, host_id):
    """Loads the chat page for a specific host."""
    host = get_object_or_404(Host, id=host_id)  # First, I get the host details
    return render(request, 'message/chatbox.html', {'host': host})  # Now, I load the chat page
