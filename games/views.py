import math

import requests
from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Game, Musts
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
        games = {}
        game_list = Game.objects.all()
        if not game_list:
            return render(request, 'games/index.html')
        items = game_list[page * 6 - 6:page * 6]
        for item in items:
            status = False
            if request.user.is_authenticated:
                if Musts.objects.filter(game=item, user=request.user).count() != 0:
                    status = True
            games[str(item.pk)] = {
                'game': {
                    'name': item.name,
                    'logo': item.logo,
                    'description': item.short_description
                },
                'status': status
            }
        total_pages = [i for i in range(1, math.ceil(Game.objects.count() / 6) + 1)]
        pages = total_pages[page - 1:5 + page - 1]
        if page > 1:
            pages.insert(0, 1)
        if page == 1 or page is None and total_pages:
            pages.append(total_pages[::-1][0])
        if page > len(total_pages):
            return HttpResponseNotFound('Страница не найдена')

        request.session['page'] = page
        context = {
            'items': games,
            'pages': pages,
        }

        return render(request, 'games/index.html', context=context)


def game(request, game_id):
    game_obj = Game.objects.filter(pk=game_id)[0]
    must_obj = None
    if request.user.is_authenticated:
        must_obj = Musts.objects.filter(game=game_obj, user=request.user).get()
    context = {
        'id': game_obj.id,
        'game': game_obj.name,
        'genres': str(game_obj.genres).split(':'),
        'platforms': str(game_obj.platforms).split(':'),
        'screenshots': str(game_obj.screenshots).split(':'),
        'ratings': {
            'users': {
                'rate': game_obj.ratings_users,
                'count': game_obj.ratings_users_count
            },
            'critics': {
                'rate': game_obj.ratings_critics,
                'count': game_obj.ratings_critics_count
            },
        },
        'tweets': get_tweets(game_obj),
        'status': bool(must_obj)
    }
    return render(request, 'games/game.html', context)


def search(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()
    title = request.GET['title']
    games = {}
    items = Game.objects.filter(name__contains=title)
    for item in items:
        if Musts.objects.filter(game=item, user=request.user).count() == 0:
            status = False
        else:
            status = True
        games[str(item.pk)] = {
            'game': {
                'name': item.name,
                'logo': item.logo,
                'description': item.short_description
            },
            'status': status
        }
    return render(request, 'games/index.html', {'items': games})


@login_required(login_url='/login')
@csrf_exempt
def must(request, game_id):
    if request.method == 'POST':
        game_obj = Game.objects.filter(id=game_id)[0]
        must_obj = Musts.objects.filter(game=game_obj, user=request.user)
        if must_obj.count() == 0:
            Musts(game=game_obj, user=request.user).save()
        else:
            must_obj[0].delete()
        return HttpResponse(status=200)


@login_required(login_url='/login')
def musts(request):
    if request.method != 'GET':
        return
    items = Musts.objects.filter(user=request.user)
    games = {str(item.pk): {
            'game': {
                'id': item.game.id,
                'name': item.game.name,
                'logo': item.game.logo,
                'genres': [i for i in item.game.genres.split(':')][:2],
            },
            'users_added': Musts.objects.filter(game=item.game).count(),
        } for item in items}
    context = {
        'items': games
    }
    return render(request, 'games/musts.html', context)
