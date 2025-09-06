from django.http import HttpResponseForbidden
from django.utils.timezone import now
from django.core.cache import cache
from ipgeolocation import IpGeoLocation
from .models import RequestLog, BlockedIP


class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = request.META.get("REMOTE_ADDR")

        # Block blacklisted IPs
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("Your IP is blocked.")

        # Cache geolocation for 24 hours
        cache_key = f"geo_{ip_address}"
        geo_data = cache.get(cache_key)

        if not geo_data:
            try:
                geo = IpGeoLocation(ip_address)
                geo_data = {
                    "country": geo.country_name,
                    "city": geo.city,
                }
                cache.set(cache_key, geo_data, timeout=60 * 60 * 24)
            except Exception:
                geo_data = {"country": None, "city": None}

        # Log request
        RequestLog.objects.create(
            ip_address=ip_address,
            timestamp=now(),
            path=request.path,
            country=geo_data.get("country"),
            city=geo_data.get("city"),
        )

        return self.get_response(request)
