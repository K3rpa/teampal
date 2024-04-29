from django.core.management.base import BaseCommand
from users.models import Message

class Command(BaseCommand):
    help = 'Deletes all messages from the database'

    def handle(self, *args, **options):
        Message.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all messages.'))
