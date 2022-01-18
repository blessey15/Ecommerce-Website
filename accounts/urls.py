from django.urls import path

from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('account/', account_view, name='account'),
]
