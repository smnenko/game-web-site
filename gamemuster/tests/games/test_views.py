import random

from django.contrib.auth.models import Permission
from django.test import TestCase

from apps.games.models import Game, Musts
from gamemuster.tests.games.factories import GameFactory
from gamemuster.tests.users.factories import CustomUserFactory, GroupFactory


class BaseTestCase(TestCase):
    def setUp(self):
        GameFactory.create_batch(size=12)
        group = GroupFactory.create()
        group.permissions.add(Permission.objects.get(name='Can view game'))
        self.user = CustomUserFactory.create(groups=(group, ))
        self.user.set_password('custompasswd')
        self.user.save()


class GameListViewTestCase(BaseTestCase):

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
        self.client.login(username=self.user.username, password='custompasswd')
        game_id = random.choice(Game.objects.all().values_list('id', flat=True))
        resp = self.client.get(f'/game/{game_id}')
        self.assertTemplateUsed(resp, 'games/game.html')

    def game_index_games_exists(self):
        resp = self.client.get('/')
        self.assertTrue(resp.context['games'])


class SearchListViewTestCase(BaseTestCase):
    def test_search_view_uses_correct_template(self):
        resp = self.client.get(f'/search?title=')
        self.assertTemplateUsed(resp, 'games/index.html')

    def test_search_view_games_exists(self):
        game = Game.objects.all().first()
        resp = self.client.get(f'/search?title={game.name}')
        self.assertTrue('page_obj' in resp.context)
        self.assertEqual(game.name, resp.context['page_obj'][0].name)

    def test_search_anonymous_without_must_btn(self):
        game = Game.objects.all().first()
        resp = self.client.get(f'/search?title={game.name}')
        self.assertContains(resp, 'style="width: 80px">Open</a>')
        self.assertNotContains(resp, 'rounded px-2 py-1" style="width: 80px">Must</button>')

    def test_search_authorized_contains_must_btn(self):
        game = Game.objects.all().first()
        self.client.force_login(self.user)
        resp = self.client.get(f'/search?title={game.name}')
        self.assertContains(resp, 'style="width: 80px">Open</a>')
        self.assertContains(resp, 'style="width: 80px">Must</button>')


class MustsListViewTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.game = Game.objects.all().first()
        Musts.objects.create(game=self.game, user=self.user)
        self.client.force_login(self.user)

    def test_must_view_uses_correct_template(self):
        resp = self.client.get('/mymusts')
        self.assertTemplateUsed(resp, 'games/musts.html')

    def test_must_view_contains_correct_game(self):
        resp = self.client.get('/mymusts')
        self.assertEqual(resp.context['musts'][0].game.name, self.game.name)

    def test_must_view_contains_unmust_btn(self):
        resp = self.client.get('/mymusts')
        self.assertContains(resp, 'position-absolute" style="top: 280px; right: 25%">UnMust</button>')
