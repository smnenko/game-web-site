import datetime

import requests
from django.core.management.base import BaseCommand

from backend.secrets import igdb_data

from games.models import Game
from games.models import Genre
from games.models import Platform
from games.models import Screenshot


class Command(BaseCommand):
    help = 'Updating games database'

    def handle(self, *args, **options):

        def add_genre(game_obj:Game, name):
            genre_ = Genre.objects.filter(name=name)
            if genre_.exists():
                genre_ = genre_.first()
            elif name:
                genre_ = Genre.objects.create(name=name)
            else:
                return

            if not game_obj.genres.filter(id=genre_.id).exists():
                game_obj.genres.add(genre_)

        def add_platform(game_obj, name):
            platform_ = Platform.objects.filter(name=name)
            if platform_.exists():
                platform_ = platform_.first()
            elif name:
                platform_ = Platform.objects.create(name=name)
            else:
                return
            if not game_obj.platforms.filter(id=platform_.id).exists():
                game_obj.platforms.add(platform_)

        def add_screenshot(game_obj, url):
            screenshot_ = Screenshot.objects.filter(url=url)
            if screenshot_.exists():
                screenshot_ = screenshot_.first()
            elif url:
                screenshot_ = Screenshot.objects.create(url=url)
            else:
                return
            if not game_obj.screenshots.filter(id=screenshot_.id).exists():
                game_obj.screenshots.add(screenshot_)

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
            cover = 'https://www.tryngo.ch/img/no-img.jpg'
            release_date = ''
            ratings_users = ''
            ratings_users_count = ''
            ratings_critics = ''
            ratings_critics_count = ''
            short_description = ''
            description = ''

            try:
                cover = game['cover']['url']
            except KeyError as e:
                print(f"An error {e.__class__.__name__} was occurred: {game['name']} не содержит поля cover")

            try:
                release_date = datetime.datetime.utcfromtimestamp(game['release_dates'][0]['date']). \
                    strftime('%B %Y')
            except KeyError as e:
                print(f"An error {e.__class__.__name__} was occurred: {game['name']} не содержит поля release_date")

            try:
                ratings_users = f"{game['rating']}"
            except KeyError as e:
                print(f"An error {e.__class__.__name__} was occurred: {game['name']} не содержит поля rating")

            try:
                ratings_users_count = f"{game['rating_count']}"
            except KeyError as e:
                print(f"An error {e.__class__.__name__} was occurred: {game['name']} не содержит поля rating_count")

            try:
                ratings_critics = f"{game['aggregated_rating']}"
            except KeyError as e:
                print(
                    f"An error {e.__class__.__name__} was occurred: {game['name']} не содержит поля aggregated_rating")

            try:
                ratings_critics_count = f"{game['aggregated_rating_count']}"
            except KeyError as e:
                print(
                    f"An error {e.__class__.__name__} was occurred: {game['name']} не содержит поля aggregated_rating_count")

            try:
                short_description = game['storyline'][:128]
            except KeyError as e:
                print(f"An error {e.__class__.__name__} was occurred: {game['name']} не содержит поля storyline")

            try:
                description = game['summary']
            except KeyError as e:
                print(f"An error {e.__class__.__name__} was occurred: {game['name']} не содержит поля summary")

            if Game.objects.filter(id=game['id']).exists():
                print(f"Database already consists {game['name']}")
            else:
                game_obj = Game.objects.create(
                    id=game['id'],
                    name=game['name'],
                    logo=cover,
                    date_release=release_date,
                    ratings_users=ratings_users,
                    ratings_users_count=ratings_users_count,
                    ratings_critics=ratings_critics,
                    ratings_critics_count=ratings_critics_count,
                    description=description,
                    short_description=short_description,
                )

                try:
                    for genre in game['genres']:
                        add_genre(game_obj, genre['name'])
                except KeyError as e:
                    print(f"An error {e.__class__.__name__} was occurred: {game['name']} не содержит поля genre")

                try:
                    for platform in game['platforms']:
                        add_platform(game_obj, platform['name'])
                except KeyError as e:
                    print(f"An error {e.__class__.__name__} was occurred: {game['name']} не содержит поля platforms")

                try:
                    for screenshot in game['screenshots']:
                        add_screenshot(game_obj, screenshot['url'])
                except KeyError as e:
                    print(f"An error {e.__class__.__name__} was occurred: {game['name']} не содержит поля screenshots")

        self.stdout.write(self.style.SUCCESS('Games successfully updated'))
