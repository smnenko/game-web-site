import requests

from backend.secrets import twitter_data


def get_tweets(game_obj):
    tweets = requests.get(
        url=twitter_data['url'] + '/tweets/search/recent',
        headers={'Authorization': 'Bearer ' + twitter_data['bearer']},
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
                url=twitter_data['url'] + f"/users/{tweet['author_id']}",
                headers={'Authorization': 'Bearer ' + twitter_data['bearer']},
                params={
                    'user.fields': 'username'
                }
            ).json()
            tweet['author_id'] = name['data']['username']

    except KeyError as e:
        tweets['message'] = 'Tweets not found'
        print(f'An error {e} was occurred')
    return tweets
