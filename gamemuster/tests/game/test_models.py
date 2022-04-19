from gamemuster.tests.game.base import (
    BaseGenreTestCase,
    BasePlatformTestCase,
    BaseScreenshotTestCase,
    BaseGameTestCase, BaseMustTestCase
)


class GenreTestCase(BaseGenreTestCase):

    def test__genre_necessary_fields_exists(self):
        genre_fields = [i.name for i in self.genre._meta.fields]

        self.assertIn('name', genre_fields)
        self.assertIn('created_at', genre_fields)
        self.assertIn('updated_at', genre_fields)

    def test__fields_length(self):
        name_max_length = self.genre._meta.get_field('name').max_length

        self.assertEqual(name_max_length, 128)


class PlatformTestCase(BasePlatformTestCase):

    def test__platform_necessary_fields_exists(self):
        platform_fields = [i.name for i in self.platform._meta.fields]

        self.assertIn('name', platform_fields)
        self.assertIn('created_at', platform_fields)
        self.assertIn('updated_at', platform_fields)

    def test_fields_length(self):
        name_max_length = self.platform._meta.get_field('name').max_length

        self.assertEqual(name_max_length, 128)


class ScreenshotTestCase(BaseScreenshotTestCase):

    def test__screenshot_necesary_fields_exists(self):
        screenshot_fields = [i.name for i in self.screenshot._meta.fields]

        self.assertIn('url', screenshot_fields)
        self.assertIn('created_at', screenshot_fields)
        self.assertIn('updated_at', screenshot_fields)


class GameTestCase(BaseGameTestCase):

    def test_game_necessary_fields_exists(self):
        game_fields = [i.name for i in self.game._meta.fields]

        self.assertIn('name', game_fields)
        self.assertIn('logo', game_fields)
        self.assertIn('storyline', game_fields)
        self.assertIn('description', game_fields)
        self.assertIn('rating', game_fields)

    def test_fields_length(self):
        name_max_length = self.game._meta.get_field('name').max_length
        storyline_max_length = self.game._meta.get_field('storyline').max_length
        description_max_length = self.game._meta.get_field('description').max_length

        self.assertEqual(name_max_length, 128)
        self.assertEqual(storyline_max_length, 256)
        self.assertEqual(description_max_length, 2048)


class MustsTestCase(BaseMustTestCase):

    def test__must_necessary_fields_exists(self):
        must_fields = [i.name for i in self.must._meta.fields]

        self.assertIn('user', must_fields)
        self.assertIn('game', must_fields)
        self.assertIn('created_at', must_fields)
        self.assertIn('updated_at', must_fields)
