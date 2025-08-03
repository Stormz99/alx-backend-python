from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
import json

@csrf_protect
@require_http_methods(["DELETE"])
def delete_user(request):
    try:
        body = json.loads(request.body)
        username = body.get("username")
        user = User.objects.get(username=username)
        user.delete()
        return JsonResponse({"message": "User deleted successfully."})
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
