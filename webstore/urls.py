from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # Leave as empty string for base url
    path('',views.home_view,name="homeview"),
    path('store/', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('payment/', views.paypal,name="payment"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('update_profile/',views.customer_profile,name='profile'),
]
