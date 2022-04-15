from django.urls import path

from . import views


urlpatterns = [
    path('', views.GameListView.as_view(), name='games'),
    path('<int:pk>', views.GameView.as_view(), name='game'),
    path('<int:pk>/delete', views.GameDeleteView.as_view(), name='game_delete'),
    path('musts', views.MustsListView.as_view(), name='musts'),
    path('<int:pk>/must', views.MustView.as_view(), name='must'),
    path('search', views.SearchListView.as_view(), name='search'),
]
