from django.core.management.base import BaseCommand

from user.models import Avatar


class Command(BaseCommand):
    help = 'Command load base avatar'

    def handle(self, *args, **options):
        if not Avatar.objects.filter(id=1):
            Avatar().save()
            self.stdout.write(self.style.SUCCESS('Default avatar loads'))
        self.stdout.write(self.style.SUCCESS('Avatar exists'))
