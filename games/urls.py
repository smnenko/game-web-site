from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('page/<int:page>', views.index),
    path('game/<int:game_id>', views.game),
    path('mymusts', views.musts),
    path('must/<int:game_id>', views.must),
    path('search', views.search)
]
