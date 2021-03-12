import math

import requests
from django.shortcuts import render
from django.http import HttpResponseNotFound

from .models import Game, Screenshot
from backend.secrets import twitter_data

# Create your views here.


def index(request, page=1):
    if request.method == 'GET':
        items = Game.objects.all()[page * 6 - 6:page * 6]
        total_pages = range(1, math.ceil(Game.objects.count() / 6) + 1)
        print(total_pages)
        if page > len(total_pages):
            return HttpResponseNotFound('Страница не найдена')

        request.session['page'] = page
        context = {
            'items': items,
            'pages': total_pages,
            'filter': True
        }

        return render(request, 'games/index.html', context=context)


def game(request, game_id):
    game = Game.objects.filter(pk=game_id)[0]

    tweets = requests.get(
        url=twitter_data['url'],
        headers={'Authorization': 'Bearer ' + twitter_data['bearer']},
        params={
            'query': '#' + ''.join([i for i in game.name if i.isalnum()]).lower(),
            'tweet.fields': 'text',
            'user.fields': 'name'
        }
    ).json()

    context = {
        'item': game,
        'screenshots': Screenshot.objects.filter(game_id=game)[:6],
        'tweets': tweets
    }
    return render(request, 'games/game.html', context)
