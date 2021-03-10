import math

from django.shortcuts import render
from django.http import HttpResponseNotFound
from TwitterSearch import *

from .models import Game, Screenshot

# Create your views here.


def index(request, page=1):
    if request.method == 'GET':
        items = Game.objects.all()[page * 6 - 6:page * 6 - 3]
        total_pages = range(1, math.ceil(items.count() / 6) + 1)
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
    context = {
        'item': game,
        'screenshots': Screenshot.objects.filter(game_id=game)[:6]
    }
    return render(request, 'games/game.html', context)
