from celery import shared_task
from django.utils.timezone import now, timedelta
from ip_tracking.models import RequestLog, SuspiciousIP

@shared_task
def detect_suspicious_ips():
    """
    Task to detect suspicious IPs based on request logs"""
    one_hour_ago = now() - timedelta(hours=1)

    # IPs with > 100 requests in the last hour
    high_traffic_ips = (
        RequestLog.objects.filter(timestamp__gte=one_hour_ago)
        .values('ip_address')
        .annotate(hit_count=models.Count('id'))
        .filter(hit_count__gt=100)
    )

    for ip_entry in high_traffic_ips:
        SuspiciousIP.objects.get_or_create(
            ip_address=ip_entry['ip_address'],
            reason="More than 100 requests in the last hour"
        )
    
    # IPS hitting sensitve endpoints
    sensitive_paths = ['/admin', '/login']
    flagged = (
        RequestLog.objects.filter(timestamp__gte=one_hour_ago, path__in=sensitive_paths)
        .values_list('ip_address', flat=True)
        .distinct()
    )

    for ip_address in flagged:
        SuspiciousIP.objects.get_or_create(
            ip_address=ip_address,
            reason='Accessed sensitive endpoints'
        )

    return f"{len(high_traffic_ips)} high traffic IPS + {len(flagged)} sensitive path IPs"