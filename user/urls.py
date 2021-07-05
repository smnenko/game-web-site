from django.urls import path
from . import views

urlpatterns = [
    path('login', views.LoginFormView.as_view()),
    path('signup', views.SignupFormView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('profile', views.ProfileListView.as_view())
]
