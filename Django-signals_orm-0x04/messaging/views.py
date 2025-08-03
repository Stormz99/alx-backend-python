from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Prefetch
from .models import Message
import json


@login_required
@csrf_exempt
def send_message(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        content = data.get("content")
        receiver_id = data.get("receiver")
        parent_id = data.get("parent_message")

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

        return JsonResponse({
            "message": "Message sent successfully",
            "id": message.id
        })

    return JsonResponse({"error": "Invalid request method"}, status=405)


@login_required
def inbox(request):
    messages = (
        Message.objects
        .filter(receiver=request.user, parent_message__isnull=True)
        .select_related('sender', 'receiver')
        .prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
        )
        .order_by('-created_at')
    )
    return render(request, 'messaging/inbox.html', {'messages': messages})


@login_required
def unread_inbox(request):
    unread_messages = (
        Message.unread
        .for_user(request.user)
    )
    return render(request, 'messaging/inbox.html', {'messages': unread_messages})


@login_required
def threaded_conversation(request, message_id):
    def get_replies_recursive(message):
        replies = (
            Message.objects
            .filter(parent_message=message)
            .select_related('sender', 'receiver')
        )
        return [
            {
                'message': reply,
                'replies': get_replies_recursive(reply)
            }
            for reply in replies
        ]

    root_message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver'),
        id=message_id
    )

    thread = {
        'message': root_message,
        'replies': get_replies_recursive(root_message)
    }

    return render(request, 'messaging/threaded_conversation.html', {'thread': thread})
