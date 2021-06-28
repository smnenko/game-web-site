import datetime

import requests
from django.core.management.base import BaseCommand

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
            ratings_users_count = ''
            ratings_critics = ''
            ratings_critics_count = ''
            short_description = ''
            description = ''

            try:
                for genre in game['genres']:
                    genres.append(genre['name'])
            except KeyError as e:
                print(f"An error {e} was occurred: {game['name']} doesn't contains field genre")

            try:
                for platform in game['platforms']:
                    platforms.append(platform['name'])
            except KeyError as e:
                print(f"An error {e} was occurred: {game['name']} doesn't contains field platforms")

            try:
                for screenshot in game['screenshots']:
                    screenshots.append(screenshot['url'])
            except KeyError as e:
                print(f"An error {e} was occurred: {game['name']} doesn't contains field screenshots")

            try:
                cover = game['cover']['url']
            except KeyError as e:
                print(f"An error {e} was occurred: {game['name']} doesn't contains field cover")

            try:
                release_date = datetime.datetime.utcfromtimestamp(game['release_dates'][0]['date']).\
                    strftime('%B %Y')
            except KeyError as e:
                print(f"An error {e} was occurred: {game['name']} doesn't contains field release_date")

            try:
                ratings_users = f"{game['rating']}"
            except KeyError as e:
                print(f"An error {e} was occurred: {game['name']} doesn't contains field rating")

            try:
                ratings_users_count = f"{game['rating_count']}"
            except KeyError as e:
                print(f"An error {e} was occurred: {game['name']} doesn't contains field rating_count")

            try:
                ratings_critics = f"{game['aggregated_rating']}"
            except KeyError as e:
                print(f"An error {e} was occurred: {game['name']} doesn't contains field aggregated_rating")

            try:
                ratings_critics_count = f"{game['aggregated_rating_count']}"
            except KeyError as e:
                print(f"An error {e} was occurred: {game['name']} doesn't contains field aggregated_rating_count")

            try:
                short_description = game['storyline'][:128]
            except KeyError as e:
                print(f"An error {e} was occurred: {game['name']} doesn't contains field storyline")

            try:
                description = game['summary']
            except KeyError as e:
                print(f"An error {e} was occurred: {game['name']} doesn't contains field summary")

            if Game.objects.filter(id=game['id']).exists():
                print(f"Database already consists {game['name']}")
            else:
                Game(
                    id=game['id'],
                    name=game['name'],
                    logo=cover,
                    genres=':'.join(genres),
                    platforms=':'.join(platforms),
                    screenshots=':'.join(screenshots),
                    date_release=release_date,
                    ratings_users=ratings_users,
                    ratings_users_count=ratings_users_count,
                    ratings_critics=ratings_critics,
                    ratings_critics_count=ratings_critics_count,
                    description=description,
                    short_description=short_description,
                ).save()

        self.stdout.write(self.style.SUCCESS('Games successfully updated'))
