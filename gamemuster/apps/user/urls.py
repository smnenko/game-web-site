from django.urls import path

from . import views

urlpatterns = [
    path('login', views.LoginFormView.as_view(), name='login'),
    path('signup', views.SignupFormView.as_view(), name='signup'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('profile', views.ProfileListView.as_view(), name='profile'),
    path('profile/update_user', views.UpdateUserFormView.as_view(), name='profile_update'),
]
