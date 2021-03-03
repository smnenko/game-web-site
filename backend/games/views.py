from django.shortcuts import render
from django.http import HttpResponseNotFound
import math

# Create your views here.

items_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]


def index(request, page=1):
    if request.method == 'GET':

        total_pages = range(1, math.ceil(len(items_list) / 6) + 1)
        if page > len(total_pages):
            return HttpResponseNotFound('Страница не найдена')

        request.session['page'] = page

        context = {
            'items': items_list[page * 6 - 6:page * 6],
            'filter': True,
            'pages': total_pages
        }

        return render(request, 'games/index.html', context=context)
