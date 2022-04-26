from unittest.mock import patch

from game.utils import GameTweetsParser
from gamemuster.tests.game.base import BaseGameViewTestCase


class GameListViewTestCase(BaseGameViewTestCase):

    def test__view_index_url_exists(self):
        resp = self.client.get(self.games_url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'game/games.html')

    @patch.object(GameTweetsParser, 'parse')
    def test__view_game_url_exists_and_dont_available_without_auth(self, tweets_func):
        resp = self.client.get(self.game_url)

        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, f'{self.login_url}?next={self.game_url}')

    @patch.object(GameTweetsParser, 'parse')
    def test__game_view_uses_correct_template(self, tweets_func):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(self.game_url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'game/game.html')

    @patch.object(GameTweetsParser, 'parse')
    def test__game_view_parsing_tweets(self, tweets_func):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(self.game_url)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(tweets_func.called)

    def test__games_pagination(self):
        resp = self.client.get(self.games_url)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('page_obj', resp.context)
        self.assertTrue(resp.context['page_obj'])


class MustsListViewTestCase(BaseGameViewTestCase):

    def test_must_view_uses_correct_template(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.musts_url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'game/musts.html')

    def test_must_view_contains_correct_game(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.musts_url)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('musts_list', resp.context)
        self.assertEqual(
            resp.context['musts_list'][0].game.name,
            self.game.name
        )

    def test_must_view_contains_unmust_btn(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.musts_url)

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'UnMust')