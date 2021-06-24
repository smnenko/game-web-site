from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('login', views.log_in),
    path('signup', views.sign_up),
    path('logout', views.log_out),
    path('profile', views.profile),
    path('mymusts', views.mymusts),
    path('profile/update_user', views.update_user)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
