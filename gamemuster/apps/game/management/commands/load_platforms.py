from django.core.management.base import BaseCommand

from game.models import Platform
from game.utils import IGDBPlatformParser


class Command(BaseCommand):
    help = 'Updating games database'

    def handle(self, *args, **options):
        self.stdout.write(
            f"{self.style.NOTICE('COMMAND')}"
            f" | "
            f"{self.style.WARNING('Platforms loading...')}"
        )

        parser = IGDBPlatformParser()
        platforms = parser.parse()

        created = Platform.objects.bulk_create(
            [Platform(id=i['id'], name=i['name']) for i in platforms]
        )

        self.stdout.write(
            f"{self.style.NOTICE('COMMAND')}"
            f" | "
            f"{self.style.SUCCESS(f'{len(created)} platforms successfully loaded')}"
        )
