from django.urls import path

from . import views


urlpatterns = [
    path('', views.IndexListView.as_view()),
    path('page/<int:page>', views.IndexListView.as_view()),
    path('game/<int:game_id>', views.GameListView.as_view()),
    path('mymusts', views.MustsListView.as_view()),
    path('must/<int:game_id>',views.MustView.as_view()),
    path('search', views.SearchListView.as_view())
]
