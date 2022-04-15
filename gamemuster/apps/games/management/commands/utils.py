import datetime

from games.models import Genre
from games.models import Platform
from games.models import Screenshot


def add_genre(name):
    genre_ = Genre.objects.filter(name=name).first()
    if not genre_:
        genre_ = Genre(name=name)
    return genre_


def add_platform(name):
    platform_ = Platform.objects.filter(name=name).first()
    if not platform_:
        platform_ = Platform(name=name)
    return platform_


def add_screenshot(url):
    screenshot_ = Screenshot.objects.filter(url=url).first()
    if not screenshot_:
        screenshot_ = Screenshot(url=url)
    return screenshot_


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


def update_game_gps(game_dict_):
    fields_list = ['genres', 'platforms', 'screenshots']
    genres_list, platforms_list, screenshots_list = [], [], []
    for field in fields_list:
        for value in game_dict_.get(field, {}):
            if field == 'genres' and value:
                genres_list.append(add_genre(value['name']))
            elif field == 'platforms' and value:
                platforms_list.append(add_platform(value['name']))
            elif field == 'screenshots' and value:
                screenshots_list.append(add_screenshot(value['url']))

    return genres_list, platforms_list, screenshots_list


def delete_exists_elements(*args):
    list_of_lists = [args[0][:], args[1][:], args[2][:]]
    list_of_objects = []
    for list_ in list_of_lists:
        if list_:
            if isinstance(list_[0], Screenshot):
                list_of_objects.append([i for i in list_ if i.url in filter_exists_elements_by_url(list_)])
            else:
                list_of_objects.append([i for i in list_ if i.name in filter_exists_elements_by_name(list_)])
    return list_of_objects


def filter_exists_elements_by_name(list_):
    obj_names = [i.name for i in list_]
    b_names = type(list_[0]).objects.filter(name__in=obj_names).values_list('name', flat=True)
    return [i for i in obj_names if i not in b_names]


def filter_exists_elements_by_url(list_):
    obj_urls = [i.url for i in list_]
    b_urls = type(list_[0]).objects.filter(url__in=obj_urls).values_list('url', flat=True)
    return [i for i in obj_urls if i not in b_urls]
