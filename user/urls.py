from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('login', views.LoginFormView.as_view()),
    path('signup', views.SignupFormView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('profile', views.ProfileListView.as_view()),
    path('profile/update_user', views.UpdateUserFormView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
