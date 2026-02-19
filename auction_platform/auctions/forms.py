from django import forms
from .models import Auction, AuctionImage


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'description', 'start_price', 'end_time']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter auction title'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Enter auction description'
            }),
            'start_price': forms.NumberInput(attrs={
                'placeholder': 'Enter starting price'
            }),
            'end_time': forms.DateTimeInput(attrs={
                'placeholder': 'YYYY-MM-DD HH:MM:SS (e.g. 2026-03-25 18:30:00)'
            }),
        }


class AuctionImageForm(forms.ModelForm):
    class Meta:
        model = AuctionImage
        fields = ['image']
