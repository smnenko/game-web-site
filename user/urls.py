from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import log_in, sign_up, log_out, profile, mymusts

urlpatterns = [
    path('login', log_in),
    path('signup', sign_up),
    path('logout', log_out),
    path('profile', profile),
    path('mymusts', mymusts),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
