import requests
from django.conf import settings
from django.core.cache import cache

from game.models import Game, Rating


def _clear_name(name: str):
    return ''.join(i for i in name if i.isalnum()).lower()


class Tweet:
    def __init__(self, author, text, created_at):
        self.author = author
        self.text = text
        self.created_at = created_at


class GameTweetsParser:
    API = 'https://api.twitter.com/2'
    TWEETS_URL = API + '/tweets/search/recent'
    AUTHOR_URL = API + '/users/{}'
    HEADERS = {'Authorization': f'Bearer {settings.TWITTER_BEARER}'}

    def _parse_author(self, author_id: int):
        params = {'user.fields': 'username'}
        response = requests.get(
            self.AUTHOR_URL.format(author_id),
            headers=self.HEADERS,
            params=params
        )
        if response.status_code == 200:
            return response.json()['data']['username']

    def _parse(self, game_name: str):
        params = {
            'query': f'#{_clear_name(game_name)}',
            'tweet.fields': 'text,created_at,author_id',
        }
        response = requests.get(
            self.TWEETS_URL,
            headers=self.HEADERS,
            params=params
        )
        tweets = []
        if response.status_code == 200:
            data = response.json()['data']
            for tweet in data:
                author = self._parse_author(tweet['author_id'])
                tweets.append(
                    Tweet(author, tweet['text'], tweet['created_at'])
                )
        return tweets

    def parse(self, game_name: str):
        if cache.get(f'{game_name}__tweets'):
            return cache.get(f'{game_name}__tweets')

        tweets = self._parse(game_name)
        cache.set(f'{game_name}__tweets', tweets, 60 * 10)
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
        response = requests.get(self.URL, data=data)
        if response.status_code == 200:
            data = response.json()['data']
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


class IGDBPlatformParser(IGDBParser):

    def __init__(self):
        super().__init__()
        self.url = self.API + 'platforms'

    def parse(self):
        response = requests.get(
            self.url,
            headers=self.headers,
            params={'fields': 'id,name'}
        )
        if response.status_code == 200:
            return response.json()['data']


class IGDBGenreParser(IGDBParser):

    def __init__(self):
        super().__init__()
        self.url = self.API + 'id,genres'

    def parse(self):
        response = requests.get(
            self.url,
            headers=self.headers,
            params={'fields': 'name'}
        )
        if response.status_code == 200:
            return response.json()['data']


class IGBDGameParser(IGDBParser):

    def __init__(self, limit: int = 0, offset: int = 0):
        super().__init__()
        self.url = self.API + 'games'
        self.limit = limit
        self.offset = offset

    def parse(self):
        params = {
            'fields': (
                'name,cover.url,genres.id,platforms.id,'
                'screenshots.url,release_dates.date,aggregated_rating,'
                'aggregated_rating_count,rating,rating_count,total_rating,'
                'total_rating_count,storyline,summary,websites'
            ),
            'limit': self.limit,
            'offset': self.offset
        }
        response = requests.get(self.url, params=params)
        if response.status_code == 200:
            games = []
            data = response.json()['data']
            for game in data:
                games.append(Game(
                    id=game['id'],
                    name=game['name'],
                    logo=game['cover']['url'],
                    storyline=game['storyline'],
                    description=game['summary'],
                    release_date=game['release_dates']['date'],
                    rating=Rating.objects.create(
                        users=game['rating'],
                        users_count=game['rating_count'],
                        critics=game['aggregated_rating'],
                        critics_count=game['aggregated_rating_count'],
                        total=game['total_rating'],
                        total_count=game['total_rating_count']
                    )
                ))
            created_games = Game.objects.bulk_create(games)
            for game in created_games:
                game.genres.set(data[str(game.id)]['genres'])
                game.platforms.set(data[str(game.id)]['platforms'])
            return Game.objects.bulk_update(fields=('genres', 'platforms'))

