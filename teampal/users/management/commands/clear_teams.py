from django.core.management.base import BaseCommand
from users.models import Team  # Adjust the import according to your project structure

class Command(BaseCommand):
    help = 'Clears all teams from the database'

    def handle(self, *args, **options):
        Team.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully Clears all teams.'))
