import random

from django.test import TestCase

from games.tests.factories import GameFactory
from games.models import Game
from user.models import CustomUser


class GameListViewTestCase(TestCase):
    def setUp(self):
        number_of_games = 12
        GameFactory.create_batch(number_of_games)

    def test_view_index_url_exists(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_index_uses_correct_template(self):
        resp = self.client.get('/')
        self.assertTemplateUsed(resp, 'games/index.html')

    def test_view_game_url_exists(self):
        game_id = random.choice(Game.objects.all().values_list('id', flat=True))
        resp = self.client.get(f'/game/{game_id}')
        self.assertEqual(resp.status_code, 200)

    def test_game_view_uses_correct_template(self):
        game_id = random.choice(Game.objects.all().values_list('id', flat=True))
        resp = self.client.get(f'/game/{game_id}')
        self.assertTemplateUsed(resp, 'games/game.html')

    def game_index_games_exists(self):
        resp = self.client.get('/')
        self.assertTrue(resp.context['games'])


class SearchListViewTestCase(TestCase):
    def test_search_view_uses_correct_template(self):
        resp = self.client.get(f'/search?title=')
        self.assertTemplateUsed(resp, 'games/index.html')

    def test_search_view_games_exists(self):
        game_name = 'Super Mario Bros.'
        resp = self.client.get(f'/search?title={game_name}')
        self.assertTrue('page_obj' in resp.context)


class MustsListViewTestCase(TestCase):
    def setUp(self):
        CustomUser(username='custom', password='custompasswd')
