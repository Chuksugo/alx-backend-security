from .models import RequestLog
from django.utils.timezone import now

class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get IP address
        ip_address = request.META.get('REMOTE_ADDR')
        # Log request
        RequestLog.objects.create(
            ip_address=ip_address,
            timestamp=now(),
            path=request.path
        )
        # Continue with response
        response = self.get_response(request)
        return response
