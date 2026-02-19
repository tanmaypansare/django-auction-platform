from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from auctions.models import Auction
from bids.models import Bid

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')

from django.contrib.auth.decorators import login_required
from auctions.models import Auction
from bids.models import Bid

@login_required
def dashboard(request):
    my_auctions = Auction.objects.filter(seller=request.user)
    my_bids = Bid.objects.filter(bidder=request.user)

    return render(request, 'dashboard.html', {
        'my_auctions': my_auctions,
        'my_bids': my_bids
    })



@login_required
def dashboard(request):
    user = request.user

    # Auctions user created
    my_auctions = Auction.objects.filter(seller=user)

    # Auctions user won
    won_auctions = Auction.objects.filter(
        winner=user,
        is_active=False
    ).count()

    # Auctions user participated in
    participated_auctions = Auction.objects.filter(
        bid__bidder=user,
        is_active=False
    ).distinct()

    # Auctions user lost
    lost_auctions = participated_auctions.exclude(winner=user).count()

    my_bids = Bid.objects.filter(bidder=user)

    return render(request, 'dashboard.html', {
        'my_auctions': my_auctions,
        'my_bids': my_bids,
        'won_auctions': won_auctions,
        'lost_auctions': lost_auctions,
    })


@login_required
def won_auctions(request):
    auctions = Auction.objects.filter(
        winner=request.user,
        is_active=False
    )
    return render(request, 'won_auctions.html', {'auctions': auctions})


@login_required
def lost_auctions(request):
    auctions = Auction.objects.filter(
        bid__bidder=request.user,
        is_active=False
    ).exclude(winner=request.user).distinct()

    return render(request, 'lost_auctions.html', {'auctions': auctions})
