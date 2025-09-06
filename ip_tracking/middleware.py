from django.http import HttpResponseForbidden
from django.utils.timezone import now
from .models import RequestLog, BlockedIP


class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = request.META.get('REMOTE_ADDR')

        # Check if IP is blocked
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("Your IP is blocked.")

        # Log request
        RequestLog.objects.create(
            ip_address=ip_address,
            timestamp=now(),
            path=request.path
        )

        return self.get_response(request)
