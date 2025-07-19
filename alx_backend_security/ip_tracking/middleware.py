import logging
from django.utils import timezone
from .models import RequestLog

# Set up logging
logger = logging.getLogger(__name__)

class IPTrackingMiddleware:
    """
    Middleware to log the IP address and the path of each request."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = request.META.get('REMOTE_ADDR', '')
        path = request.path
        logger.info(f"Request from IP: {ip_address} at path: {path}")

        # Save the request log to the database
        RequestLog.objects.create(ip_address=ip_address, path=path, timestamp=timezone.now())
        response = self.get_response(request)
        return response
    
    