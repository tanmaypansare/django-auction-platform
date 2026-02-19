from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Auction, AuctionImage
from .forms import AuctionForm, AuctionImageForm
from bids.forms import BidForm
from bids.models import Bid

from bids.models import Bid

def home(request):
    auctions = Auction.objects.all()

    for auction in auctions:
        if auction.is_active and auction.end_time <= timezone.now():
            auction.is_active = False

            highest = Bid.objects.filter(auction=auction).order_by('-amount').first()
            if highest:
                auction.winner = highest.bidder

            auction.save()

    active_auctions = Auction.objects.filter(is_active=True)

    return render(request, 'home.html', {'auctions': active_auctions})



@login_required
def create_auction(request):
    if request.method == 'POST':
        form = AuctionForm(request.POST)
        image_form = AuctionImageForm(request.POST, request.FILES)

        if form.is_valid() and image_form.is_valid():
            auction = form.save(commit=False)
            auction.seller = request.user
            auction.save()

            img = image_form.save(commit=False)
            img.auction = auction
            img.save()

            return redirect('my_auctions')
    else:
        form = AuctionForm()
        image_form = AuctionImageForm()

    return render(request, 'create_auction.html', {
        'form': form,
        'image_form': image_form
    })


@login_required
def my_auctions(request):
    auctions = Auction.objects.filter(seller=request.user)
    return render(request, 'my_auctions.html', {'auctions': auctions})


def auction_detail(request, id):
    auction = Auction.objects.get(id=id)
    bids = Bid.objects.filter(auction=auction).order_by('-amount')
    highest_bid = bids.first()

    bid_form = BidForm()

    if request.method == 'POST' and request.user.is_authenticated:
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            bid = bid_form.save(commit=False)
            bid.auction = auction
            bid.bidder = request.user

            if highest_bid is None or bid.amount > highest_bid.amount:
                bid.save()
            else:
                return render(request, 'auction_detail.html', {
                    'auction': auction,
                    'bids': bids,
                    'form': bid_form,
                    'error': 'Bid must be higher than current highest bid'
                })

    return render(request, 'auction_detail.html', {
        'auction': auction,
        'bids': bids,
        'form': bid_form
    })

