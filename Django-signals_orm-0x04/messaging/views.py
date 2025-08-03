from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
import json


@csrf_exempt
@login_required
def send_message(request):
    if request.method == "POST":
        data = json.loads(request.body)

        content = data.get("content")
        receiver_id = data.get("receiver")
        parent_id = data.get("parent_message")  # Optional

        if not content or not receiver_id:
            return JsonResponse({"error": "Missing required fields"}, status=400)

        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "Receiver not found"}, status=404)

        parent_message = None
        if parent_id:
            try:
                parent_message = Message.objects.get(id=parent_id)
            except Message.DoesNotExist:
                return JsonResponse({"error": "Parent message not found"}, status=404)

        message = Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
            parent_message=parent_message
        )

        return JsonResponse({"message": "Message sent successfully", "id": message.id})
