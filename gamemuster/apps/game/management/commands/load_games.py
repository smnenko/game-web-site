from datetime import datetime

from django.core.management.base import BaseCommand

from game.models import Game, Rating, Screenshot
from game.utils import IGDBGameParser


class Command(BaseCommand):
    help = 'Updating games database'

    def log(self, message):
        self.stdout.write(
            f"{self.style.NOTICE('COMMAND')}"
            f" | "
            f"{self.style.SUCCESS(message)}"
        )

    def handle(self, *args, **options):
        self.log('Games loading...')

        existing_games = Game.objects.values_list('id', flat=True)
        games_to_add = []

        parser = IGDBGameParser(limit=20)
        games = parser.parse()

        self.log('Response successfully received')

        games = [i for i in games if i['id'] not in existing_games]

        for game in games:
            if 'cover' in game:
                game['cover']['url'] = game['cover']['url'].replace('t_thumb', 't_cover_big')
            else:
                game.update({'cover': {'url': None}})

            if 'screenshots' in game:
                game['screenshots'] = [
                    i['url'].replace('t_thumb', 't_original')
                    for i in game['screenshots']
                ]

            rating = None
            if (
                'rating' in game or
                'rating_count' in game or
                'aggregated_rating' in game or
                'aggregated_rating_count' in game or
                'total_rating' in game or
                'total_rating_count' in game
            ):
                rating = Rating.objects.create(
                    users=game.get('rating'),
                    users_count=game.get('rating_count'),
                    critics=game.get('aggregated_rating'),
                    critics_count=game.get('aggregated_rating_count'),
                    total=game.get('total_rating'),
                    total_count=game.get('total_rating_count')
                )

            release_date = None
            if 'release_dates' in game:
                release_date = datetime.fromtimestamp(
                    min(i['date'] for i in game['release_dates'])
                ).date()

            games_to_add.append(Game(
                id=game['id'],
                name=game['name'],
                cover=game['cover']['url'],
                storyline=game.get('storyline'),
                description=game.get('summary'),
                date_release=release_date,
                rating=rating
            ))

        created_games = Game.objects.bulk_create(games_to_add)
        for i, game in enumerate(created_games):
            [Screenshot.objects.create(game=game, url=x) for x in games[i].get('screenshots', [])]
            game.genres.set(x['id'] for x in games[i].get('genres', []))
            game.platforms.set(x['id'] for x in games[i].get('platforms', []))

        self.log(f'{len(games_to_add)} games successfully loaded')
