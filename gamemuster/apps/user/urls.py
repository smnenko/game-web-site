from django.urls import path

from . import views

urlpatterns = [
    path('login', views.LoginFormView.as_view(), name='login'),
    path('signup', views.SignupFormView.as_view(), name='signup'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('<int:pk>', views.ProfileView.as_view(), name='profile'),
    path('<int:pk>/update', views.UpdateUserFormView.as_view(), name='profile_update'),
]
