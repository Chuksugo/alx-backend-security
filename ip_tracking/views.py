from django.http import JsonResponse
from ratelimit.decorators import ratelimit

# Anonymous users: 5 requests/minute per IP
@ratelimit(key="ip", rate="5/m", block=True)
def anonymous_login(request):
    return JsonResponse({"message": "Anonymous login attempt"})

# Authenticated users: 10 requests/minute per IP
@ratelimit(key="ip", rate="10/m", block=True)
def user_login(request):
    if request.user.is_authenticated:
        return JsonResponse({"message": f"Welcome {request.user.username}"})
    return JsonResponse({"error": "Authentication required"}, status=401)
