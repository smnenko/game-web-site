from datetime import datetime

import requests
from django.conf import settings
from django.core.cache import cache


class Tweet:
    def __init__(self, author, text, created_at):
        self.author = author
        self.text = text
        self.created_at = created_at


class GameTweetsParser:
    URL = 'https://twitter.com'
    API = 'https://api.twitter.com/2'
    WIDGET_URL = 'https://publish.twitter.com/oembed'
    TWEETS_URL = API + '/tweets/search/recent'
    AUTHOR_URL = API + '/users/{}'
    HEADERS = {'Authorization': f'Bearer {settings.TWITTER_BEARER}'}

    @staticmethod
    def _clear_name(name: str):
        return ''.join(i for i in name if i == ' ' or i.isalpha() or i.isdigit())

    def _parse(self, game_name: str):
        params = {
            'query': f'{game_name}',
            'expansions': 'author_id,entities.mentions.username',
            'user.fields': 'created_at'
        }
        response = requests.get(
            self.TWEETS_URL,
            headers=self.HEADERS,
            params=params
        )
        if response.status_code == 200:
            response = response.json()
            if 'data' in response:
                return [
                    f"{self.URL}/{i['entities']['mentions'][0]['username']}/status/{i['id']}"
                    for i in response['data']
                    if 'entities' in i
                ]
        return []

    def get_widgets(self, game_name: str):
        return [
            requests.get(self.WIDGET_URL, params={'url': i, 'theme': 'dark'}).json()['html']
            for i in self.parse(game_name)
        ]

    def parse(self, game_name: str):
        clear_game_name = self._clear_name(game_name)
        if tweets := cache.get(f'{clear_game_name}__tweets'):
            return tweets

        tweets = self._parse(clear_game_name)
        cache.set(f'{clear_game_name}__tweets', tweets, 60 * 10)
        return tweets


class TwitchAuth:
    URL = 'https://id.twitch.tv/oauth2/token'
    CLIENT_ID = settings.IGDB_CLIENT_ID
    CLIENT_SECRET = settings.IGDB_CLIENT_SECRET

    def _authorization(self):
        data = {
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET,
            'grant_type': 'client_credentials'
        }
        response = requests.post(self.URL, data=data)
        if response.status_code == 200:
            data = response.json()
            return f"{data['token_type'].title()} {data['access_token']}"

    @property
    def authorization(self):
        if cache.get('TWITCH_AUTHORIZATION'):
            return cache.get('TWITCH_AUTHORIZATION')

        authorization = self._authorization()
        cache.set('TWITCH_AUTHORIZATION', authorization, 60 * 10)
        return authorization


class IGDBParser:
    API = 'https://api.igdb.com/v4/'
    CLIENT_ID = settings.IGDB_CLIENT_ID

    def __init__(self):
        self.headers = {
            'Client-ID': self.CLIENT_ID,
            'Authorization': TwitchAuth().authorization
        }
        self.response = None
        self.params = None
        self.url = None

    def parse(self):
        self.response = requests.get(
            self.url,
            headers=self.headers,
            params=self.params
        )
        if self.response.status_code == 200:
            return self.response.json()


class IGDBPlatformParser(IGDBParser):

    def __init__(self, limit: int = 500, offset: int = 0):
        super().__init__()
        self.url = self.API + 'platforms'
        self.limit = limit
        self.offset = offset
        self.params = {
            'fields': 'name',
            'limit': self.limit,
            'offset': self.offset
        }


class IGDBGenreParser(IGDBParser):

    def __init__(self, limit: int = 500, offset: int = 0):
        super().__init__()
        self.url = self.API + 'genres'
        self.limit = limit
        self.offset = offset
        self.params = {
            'fields': 'name',
            'limit': self.limit,
            'offset': self.offset
        }


class IGDBGameParser(IGDBParser):

    def __init__(self, limit: int = 500, offset: int = 0):
        super().__init__()
        self.url = self.API + 'games'
        self.limit = limit
        self.offset = offset
        self.params = {
            'fields': (
                'name,cover.url,genres.id,platforms.id,'
                'screenshots.url,release_dates.date,aggregated_rating,'
                'aggregated_rating_count,rating,rating_count,total_rating,'
                'total_rating_count,storyline,summary,websites'
            ),
            'limit': self.limit,
            'offset': self.offset
        }


