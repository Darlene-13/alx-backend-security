from django.core.management.base import BaseCommand
from ip_tracking.models import BlockedIP
# Defining the command class

class Command(BaseCommand):
    help = 'Block an IP address by adding it to the BlockedIP model'

    #Defining how to access the IP address
    def add_arguments(self, parser):
        parser.add_argument('ip_address', type=str, help='The IP address to block.')

        #Handle the command logic
    def handle(self, *args, **options):
        # Get the IP address from the command arguments
        ip_address = options['ip_address']

        #Check if the IP address is already blocked 
        if BlockedIP.objects.filter(ip_address = ip_address).exists():
            self.stdout.write(self.style.WARNING(f"IPAddress {ip_address} is already blocked."))
        else:
            # Create a new BlockedIP Instance
            blocked_ip = BlockedIP(ip_address=ip_address)
            blocked_ip.save()
            self.stdout.write(self.style.SUCCESS(f"Successfully blocked IP address: {ip_address}"))