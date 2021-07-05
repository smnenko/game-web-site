import requests
from django.core.management.base import BaseCommand

from backend.secrets import igdb_data

from games.models import Game
from .utils import create_game_dict
from .utils import update_game_gps
from .utils import delete_exists_elements


class Command(BaseCommand):
    help = 'Updating games database'

    def handle(self, *args, **options):

        twitch_data = requests.post(url='https://id.twitch.tv/oauth2/token', data=igdb_data).json()
        auth_data = {
            'Client-ID': igdb_data['client_id'],
            'Authorization': twitch_data['token_type'].title() + ' ' + twitch_data['access_token']
        }
        params = {
            'fields': ['name, cover.url, genres.name, platforms.name, screenshots.url, release_dates.date,'
                       'aggregated_rating, aggregated_rating_count,rating,rating_count,storyline,summary'],
            'limit': 500
        }
        game_list = requests.get(url='https://api.igdb.com/v4/games', headers=auth_data, params=params).json()

        for game in game_list:
            dict_init = {'cover': 'cover',
                         'release_date': 'release_dates',
                         'ratings_users': 'rating',
                         'ratings_users_count': 'rating_count',
                         'ratings_critics': 'aggregated_rating',
                         'ratings_critics_count': 'aggregated_rating_count',
                         'short_description': 'storyline',
                         'description': 'summary'
                         }

            game_dict = create_game_dict(dict_init, game)

            if Game.objects.filter(id=game['id']).exists():
                print(f"Database already consists {game['name']}")
            else:
                game_obj = Game.objects.create(
                    id=game['id'],
                    name=game['name'],
                    logo=game_dict['cover'],
                    date_release=game_dict['release_date'],
                    ratings_users=game_dict['ratings_users'],
                    ratings_users_count=game_dict['ratings_users_count'],
                    ratings_critics=game_dict['ratings_critics'],
                    ratings_critics_count=game_dict['ratings_critics_count'],
                    description=game_dict['description'],
                    short_description=game_dict['short_description'],
                )
                genres, platforms, screenshots = update_game_gps(game)

                for list_ in delete_exists_elements(genres, platforms, screenshots):
                    if list_:
                        type(list_[0]).objects.bulk_create(list_)

                game_obj.genres.set(genres)
                game_obj.platforms.set(platforms)
                game_obj.screenshots.set(screenshots)

        self.stdout.write(self.style.SUCCESS('Games successfully updated'))
