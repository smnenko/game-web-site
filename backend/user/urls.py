from django.urls import path
from .views import log_in, sign_up, log_out, profile, mymusts

urlpatterns = [
    path('login', log_in),
    path('signup', sign_up),
    path('logout', log_out),
    path('profile', profile),
    path('mymusts', mymusts),
]
