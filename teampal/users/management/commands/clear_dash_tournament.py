from django.core.management.base import BaseCommand
from users.models import TournamentPost

class Command(BaseCommand):
    help = 'Clears all TournamentPost from the database'

    def handle(self, *args, **options):
        TournamentPost.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully Clears all TournamentPost.'))