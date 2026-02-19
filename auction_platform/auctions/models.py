from django.db import models
from django.contrib.auth.models import User

class Auction(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, null=True, blank=True, related_name='won_auctions', on_delete=models.SET_NULL)

    def __str__(self):
        return self.title


class AuctionImage(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='auctions/')

    def __str__(self):
        return self.auction.title
