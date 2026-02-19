from django.urls import path
from . import views

urlpatterns = [
    path('auctions/', views.auction_list),
    path('auction/<int:id>/', views.auction_detail),
    path('bid/', views.place_bid),
    path('my-bids/<int:user_id>/', views.my_bids),
]
