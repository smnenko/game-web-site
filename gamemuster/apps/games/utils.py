import requests
import environ
from django.conf import settings
from django.db.models import Count

from .models import Musts


env = environ.Env()
environ.Env.read_env(open(settings.BASE_DIR.resolve() / '.env'))


def get_tweets(game_obj):
    tweets = requests.get(
        url='https://api.twitter.com/2' + '/tweets/search/recent',
        headers={'Authorization': 'Bearer ' + env('TWITTER_BEARER')},
        params={
            'query': '#'
                     + ''.join(i for i in game_obj.name if i.isalnum()).lower(),
            'tweet.fields': 'text,created_at,author_id',
        },
    ).json()

    try:
        tweets = tweets['data']
        for tweet in tweets:
            name = requests.get(
                url='https://api.twitter.com/2' + f"/users/{tweet['author_id']}",
                headers={'Authorization': 'Bearer ' + env('TWITTER_BEARER')},
                params={
                    'user.fields': 'username'
                }
            ).json()
            tweet['author_id'] = name['data']['username']

    except KeyError as e:
        tweets['message'] = 'Tweets not found'
    return tweets


class MustUtil:

    def __init__(self, request):
        self.request = request
        self.model = Musts
        self.queryset = {}

    def get_musts(self):
        games_count = (
            self.model.objects
                .values('game__id', 'game__name', 'game__genres__name', 'game__logo')
                .annotate(users_added=Count('game__name'))
                .order_by('game_id')
        )
        user_musts = self.model.objects.filter(user=self.request.user).values_list('game_id', flat=True)

        for i in games_count:
            if i.get('game__id') in user_musts:
                if i.get('game__id') not in self.queryset.keys():
                    self.queryset.setdefault(i['game__id'], {})
                    self.queryset.get(i['game__id']).setdefault('name', i['game__name'])
                    self.queryset.get(i['game__id']).setdefault('logo', i['game__logo'])
                    self.queryset.get(i['game__id']).setdefault('genres', []).append(i['game__genres__name'])
                    self.queryset.get(i['game__id']).setdefault('users_added', i['users_added'])
                else:
                    self.queryset.get(i['game__id']).get('genres').append(i['game__genres__name'])
        return self.queryset
