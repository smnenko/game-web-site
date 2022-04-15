from django.urls import path
from core import views

urlpatterns = [
    path('', views.IndexListView.as_view(), name='index')
]
