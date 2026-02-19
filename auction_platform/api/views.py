from rest_framework.decorators import api_view
from rest_framework.response import Response
from auctions.models import Auction
from bids.models import Bid
from .serializers import AuctionSerializer, BidSerializer
from rest_framework import status

@api_view(['GET'])
def auction_list(request):
    auctions = Auction.objects.filter(is_active=True)
    serializer = AuctionSerializer(auctions, many=True)
    return Response(serializer.data)




@api_view(['GET'])
def auction_detail(request, id):
    try:
        auction = Auction.objects.get(id=id)
    except Auction.DoesNotExist:
        return Response(
            {"error": "Auction not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = AuctionSerializer(auction)
    return Response(serializer.data)



@api_view(['POST'])
def place_bid(request):
    serializer = BidSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['GET'])
def my_bids(request, user_id):
    bids = Bid.objects.filter(bidder_id=user_id)
    serializer = BidSerializer(bids, many=True)
    return Response(serializer.data)
