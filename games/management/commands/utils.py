import datetime

from games.models import Genre
from games.models import Platform
from games.models import Screenshot


def add_genre(game_obj, name):
    genre_ = Genre.objects.filter(name=name)
    if genre_.exists():
        genre_ = genre_.first()
    elif name:
        genre_ = Genre.objects.create(name=name)
    else:
        return

    if not game_obj.genres.filter(id=genre_.id).exists():
        game_obj.genres.add(genre_)


def add_platform(game_obj, name):
    platform_ = Platform.objects.filter(name=name)
    if platform_.exists():
        platform_ = platform_.first()
    elif name:
        platform_ = Platform.objects.create(name=name)
    else:
        return
    if not game_obj.platforms.filter(id=platform_.id).exists():
        game_obj.platforms.add(platform_)


def add_screenshot(game_obj, url):
    screenshot_ = Screenshot.objects.filter(url=url)
    if screenshot_.exists():
        screenshot_ = screenshot_.first()
    elif url:
        screenshot_ = Screenshot.objects.create(url=url)
    else:
        return
    if not game_obj.screenshots.filter(id=screenshot_.id).exists():
        game_obj.screenshots.add(screenshot_)


def create_game_dict(dict_init_, game_dict_):
    new_dict = {}
    for key in dict_init_.keys():
        try:
            if key == 'cover':
                new_dict[key] = game_dict_[key]['url']
            elif key == 'release_dates':
                new_dict[key] = datetime.datetime.utcfromtimestamp(
                    game_dict_[key][0]['date']).strftime('%B %Y')
            elif key == 'storyline':
                new_dict[key] = game_dict_[key][:128]
            else:
                new_dict[key] = game_dict_[key]

        except KeyError as e:
            if key == 'cover':
                new_dict[key] = 'https://semantic-ui.com/images/wireframe/image.png'
            else:
                new_dict[key] = ''
            print(f"An error {e.__class__.__name__} was occurred: field {key} not found")

    return new_dict


def update_game_gps(game_obj_, game_dict_):
    fields_dict = {
        'genres': add_genre,
        'platforms': add_platform,
        'screenshots': add_screenshot,
    }
    for key, value in fields_dict.items():
        try:
            name = 'name'
            if key == 'screenshots':
                name = 'url'
            for something in game_dict_[key]:
                value(game_obj_, something[name])
        except KeyError as e:
            print(f"An error {e.__class__.__name__} was occurred")
