import random

from django.test import TestCase

from games.tests.factories import GameFactory
from games.models import Game
from user.tests.factories import CustomUserFactory, GroupFactory


class GameListViewTestCase(TestCase):
    def setUp(self):
        GameFactory.create_batch(size=12)
        user = CustomUserFactory.create(groups=(GroupFactory.create(),))
        user.set_password('custompasswd')
        user.save()

    def test_view_index_url_exists(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_index_uses_correct_template(self):
        resp = self.client.get('/')
        self.assertTemplateUsed(resp, 'games/index.html')

    def test_view_game_url_exists(self):
        game_id = random.choice(Game.objects.all().values_list('id', flat=True))
        resp = self.client.get(f'/game/{game_id}')
        self.assertEqual(resp.status_code, 302)

    def test_game_view_uses_correct_template(self):
        game_id = random.choice(Game.objects.all().values_list('id', flat=True))
        resp = self.client.get(f'/game/{game_id}', follow=True)
        self.assertTemplateUsed(resp, 'user/login.html')

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
