# from django.urls import path
#
# from .views import *
#
# urlpatterns = [
#     path('login/', login_view, name='login'),
#     path('register/', registration_view, name='register'),
#     path('logout/', logout_view, name='logout'),
#     path('account/', account_view, name='account'),
#     path('feedback/',feedback_view,name='feedback')
# ]
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
]