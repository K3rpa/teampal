from django.core.management.base import BaseCommand
import redis

class Command(BaseCommand):
    help = 'Clears all data from Redis'

    def handle(self, *args, **options):
        r = redis.Redis(host='127.0.0.1', port=6379, db=0)  # Adjust as necessary
        r.flushall()
        self.stdout.write(self.style.SUCCESS('Successfully cleared all Redis data.'))
