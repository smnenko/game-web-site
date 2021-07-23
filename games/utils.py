import requests
import environ
from django.conf import settings


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
