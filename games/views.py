import math

from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.views.generic.base import View
from django.db.models import Count, Case, When, Value, BooleanField
from django.utils.decorators import method_decorator

from games.models import Game
from games.models import Musts
from . import utils


class IndexListView(ListView):
    model = Game
    template_name = 'games/index.html'
    context_object_name = 'games'
    pages = []

    def get_queryset(self):
        games = self.model.objects.all()
        page = 1 if 'page' not in self.kwargs.keys() else self.kwargs['page']
        total_pages = [i for i in range(1, math.ceil(self.model.objects.count() / 6) + 1)]
        self.pages = total_pages[
                     page - 6 if page > 6 else 0: page + 6 if page < len(total_pages) - 6 else len(total_pages)]
        if not games:
            return
        if self.request.user.is_authenticated:
            musts = Musts.objects.filter(user=self.request.user).values_list('game_id', flat=True)
        else:
            musts = []
        return games.annotate(
            status=Case(When(id__in=musts, then=Value(True)), default=Value(False), output_field=BooleanField())
        )[page * 6 - 6:page * 6]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_object_name] = self.get_queryset()
        context['pages'] = self.pages
        return context


class GameListView(ListView):
    model = Game
    template_name = 'games/game.html'
    context_object_name = 'game'
    game_obj = None

    def get_queryset(self):
        self.game_obj = self.model.objects.filter(id=self.kwargs['game_id'])
        status = False
        if self.request.user.is_authenticated:
            status = Musts.objects.filter(game=self.game_obj.first(), user=self.request.user).exists()
        return self.game_obj.annotate(status=Value(status, output_field=BooleanField())).first()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context[self.context_object_name] = self.get_queryset()
        context['tweets'] = utils.get_tweets(self.game_obj.first())
        return context


class SearchListView(ListView):
    model = Game
    template_name = 'games/index.html'
    context_object_name = 'games'

    def get_queryset(self):
        musts = []
        if self.request.user.is_authenticated:
            musts = Musts.objects.filter(user=self.request.user).values_list('game_id', flat=True)
        return self.model.objects.filter(name__icontains=self.request.GET['title']).annotate(status=Case(
            When(id__in=musts, then=Value(True)), default=Value(False), output_field=BooleanField()
        ))


@method_decorator(csrf_exempt, name='dispatch')
class MustView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        game_obj = Game.objects.filter(id=self.kwargs['game_id'])
        must_obj = Musts.objects.filter(game=game_obj.first(), user=request.user)
        if must_obj.exists():
            must_obj.first().delete()
        else:
            Musts(game=game_obj.first(), user=request.user).save()
        return HttpResponse(status=200)


class MustsListView(LoginRequiredMixin, ListView):
    model = Musts
    template_name = 'games/musts.html'
    context_object_name = 'musts'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).annotate(users_added=Count('game'))
