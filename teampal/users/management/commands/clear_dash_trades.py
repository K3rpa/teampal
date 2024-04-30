from django.core.management.base import BaseCommand
from users.models import Trade

class Command(BaseCommand):
    help = 'Clears all trade from the database'

    def handle(self, *args, **options):
        Trade.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully Clears all trades.'))