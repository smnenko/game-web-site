import math

from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.db.models import Count

from games.models import Game
from games.models import Musts
from . import utils


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
                if Musts.objects.filter(game=item, user=request.user).exists():
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
        'tweets': utils.get_tweets(game_obj),
        'status': bool(must_obj)
    }
    return render(request, 'games/game.html', context)


def search(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()
    title = request.GET['title']
    games = {}
    musts = Musts.objects.filter(user=request.user).values_list('game_id', flat=True)
    items = Game.objects.filter(name__icontains=title)
    for item in items:
        games[str(item.pk)] = {
            'game': {
                'name': item.name,
                'logo': item.logo,
                'description': item.short_description
            },
            'status': item.id in musts
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


class MustsListView(LoginRequiredMixin, ListView):
    model = Musts
    template_name = 'games/musts.html'
    context_object_name = 'musts'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).annotate(users_added=Count('game'))
