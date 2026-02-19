from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('won-auctions/', views.won_auctions, name='won_auctions'),
    path('lost-auctions/', views.lost_auctions, name='lost_auctions'),


]
