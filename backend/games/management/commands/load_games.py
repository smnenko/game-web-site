import datetime

import requests
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import DataError

from backend.secrets import igdb_data

from games.models import Game


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
            genres = []
            platforms = []
            screenshots = []
            cover = 'https://www.tryngo.ch/img/no-img.jpg'
            release_date = ''
            ratings_users = ''
            ratings_critics = ''
            short_description = ''
            description = ''

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
                for screenshot in game['screenshots']:
                    screenshots.append(screenshot['url'])
            except KeyError as e:
                print(f"An error {e} was occurred: {game['name']} не содержит поля screenshots")

            try:
                cover = game['cover']['url']
            except KeyError as e:
                print(f"An error {e} was occurred: {game['name']} не содержит поля cover")

            try:
                release_date = datetime.datetime.utcfromtimestamp(game['release_dates'][0]['date']).\
                    strftime('%B %Y')
            except KeyError as e:
                print(f"An error {e} was occurred: {game['name']} не содержит поля release_date")

            try:
                ratings_users = f"{game['rating']} {game['rating_count']}"
            except KeyError as e:
                print(f"An error {e} was occurred: {game['name']} не содержит поля rating")

            try:
                ratings_critics = f"{game['aggregated_rating']} {game['aggregated_rating_count']}"
            except KeyError as e:
                print(f"An error {e} was occurred: {game['name']} не содержит поля aggregated_rating")

            try:
                short_description = game['storyline'][:128]
            except KeyError as e:
                print(f"An error {e} was occurred: {game['name']} не содержит поля storyline")

            try:
                description = game['summary']
            except KeyError as e:
                print(f"An error {e} was occurred: {game['name']} не содержит поля summary")

            Game(
                id=game['id'],
                name=game['name'],
                logo=cover, genres=':'.join(genres),
                platforms=':'.join(platforms),
                screenshots=':'.join(screenshots),
                date_release=release_date,
                ratings_users=ratings_users,
                ratings_critics=ratings_critics,
                description=description,
                short_description=short_description
            ).save()

        self.stdout.write(self.style.SUCCESS('Games successfully updated'))
