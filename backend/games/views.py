import math

import requests
from django.shortcuts import render
from django.http import HttpResponseNotFound

from .models import Game
from backend.secrets import twitter_data

# Create your views here.


def index(request, page=1):
    if request.method == 'POST':
        title = request.POST['title']
        games = Game.objects.filter(name=title)

        context = {
            'filter': False,
            'items': games
        }
        return render(request, 'games/index.html', context)
    elif request.method == 'GET':
        items = Game.objects.all()[page * 6 - 6:page * 6].filter()
        total_pages = [i for i in range(1, math.ceil(Game.objects.count() / 6) + 1)]

        pages = total_pages[page - 1:5 + page - 1]
        if page > 1:
            pages.insert(0, 1)
        if page > len(total_pages):
            return HttpResponseNotFound('Страница не найдена')

        request.session['page'] = page
        context = {
            'items': items,
            'pages': pages,
            'filter': True
        }

        return render(request, 'games/index.html', context=context)


def game(request, game_id):
    game = Game.objects.filter(pk=game_id)[0]

    tweets = requests.get(
        url=twitter_data['url'] + '/tweets/search/recent',
        headers={'Authorization': 'Bearer ' + twitter_data['bearer']},
        params={
            'query': '#' + ''.join([i for i in game.name if i.isalnum()]).lower(),
            'tweet.fields': 'text,created_at,author_id',
        }
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

    context = {
        'game': game,
        'genres': str(game.genres).split(':'),
        'platforms': str(game.platforms).split(':'),
        'screenshots': str(game.screenshots).split(':'),
        'tweets': tweets
    }
    return render(request, 'games/game.html', context)
