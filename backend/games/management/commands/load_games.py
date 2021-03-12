import requests
from django.core.management.base import BaseCommand, CommandError

from backend.backend.secrets import igdb_data

from games.models import Game


class Command(BaseCommand):
    help = 'Updating games database'

    def handle(self, *args, **options):
        twitch_data = requests.post(url='https://id.twitch.tv/oauth2/token', data=igdb_data).json()
        auth_data = {
            'Client-ID': self.data['client_id'],
            'Authorization': twitch_data['token_type'].title() + ' ' + twitch_data['access_token']
        }
        params = {
            'fields': ['name, cover.url, genres.name, platforms.name, screenshots.*'],
            'limit': 10
        }
        game_list = requests.get(url='https://api.igdb.com/v4/games', headers=auth_data, params=params).json()

        for game in game_list:
            genres = []
            platforms = []

            try:
                for genre in game['genres']:
                    genres.append(genre['name'])
            except KeyError as e:
                print(f"An error {e} was occurred: {game['name']} не содержит поля genre")

            try:
                for platform in game['platforms']:
                    platforms.append(platform['name'])
            except KeyError as e:
                print(f"An error {e} was occurred: {game['name']} не содержит поля platforms")

            try:
                cover = game['cover']['url']
            except KeyError as e:
                print(f"An error {e} was occurred: {game['name']} не содержит поля cover")

            Game(id=game['id'], name=game['name'], logo=cover, genres=' '.join(genres), platforms=' '.join(platforms)).save()

        self.stdout.write(self.style.SUCCESS('Games successfully updated'))
