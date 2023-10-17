from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
from news_db.models import Post


class Command(BaseCommand):
    help = 'Delete all the news, older than 30 days'

    requires_migrations_checks = True

    def handle(self, *args, **options):
        self.stdout.readable()
        self.stdout.write('Do You really want to delete all the news, older than 30 days? yes/no')
        answer = input()

        if answer == 'yes':
            time_delta = datetime.today() - timedelta(days=30)
            Post.objects.filter(position="NW", create_date__lt=time_delta).delete()
            self.stdout.write(self.style.SUCCESS('Succesfully deleted old news!'))
            return

        self.stdout.write(self.style.ERROR('Access denied!'))

