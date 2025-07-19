import logging
import requests
from django.utils import timezone
from django.core.cache import cache
from .models import RequestLog, BlockedIP
from django.http import HttpResponseForbidden

# Set up logging
logger = logging.getLogger(__name__)

# Helper function to get the geolocation of the IP address
def get_geo_data(ip_address):
    """
    Get the geolocation of the IP address using an external API.
    Return a dictionary with 'country and city as keys.  
    """
    if ip_address == "127.0.0.1":
        return {'country': None, 'city': None}
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        if response.status_code == 200:
            data = response.json()
            return {
                'country': data.get("country"),
                'city': data.get("city")
            }
    except Exception:
        pass
    return {'country': None, 'city': None}



class IPTrackingMiddleware:
    """
    Middleware to log the IP address and the path of each request."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = request.META.get('REMOTE_ADDR', '')
        path = request.path
        logger.info(f"Request from IP: {ip_address} at path: {path}")

        geo_data = cache.get(f"geo:{ip_address}")
        if not geo_data:
            get_data = get_geo_data(ip_address)
            cache.set(f"geo: {ip_address}, geo_data, timeout=86400")
        # Save the request log to the database
        RequestLog.objects.create(ip_address=ip_address, path=path, timestamp=timezone.now())
        response = self.get_response(request)
        return response
    
class BlockedIPMiddleware:
    """ Middleware to block requests from specific IP addresses."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = request.META.get('REMOTE_ADDR','')
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            logger.warning (f"Blocked request from IP: {ip_address}")
            return HttpResponseForbidden("Access denied for this IP address.")
        response = self.get_response(request)
        return response