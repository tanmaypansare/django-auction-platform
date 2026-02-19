from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Bid

@login_required
def my_bids(request):
    bids = Bid.objects.filter(bidder=request.user)
    return render(request, 'my_bids.html', {'bids': bids})
