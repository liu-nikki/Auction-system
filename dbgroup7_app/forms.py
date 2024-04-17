from django import forms
from .models import Paymentinfo, Shipping, Bid, Category

class PaymentInfoForm(forms.ModelForm):
    class Meta:
        model = Paymentinfo
        fields = ['payment_method', 'billing_address']

class ShippingForm(forms.ModelForm):
    class Meta:
        model = Shipping
        fields = ['shipping_address', 'shipping_date']

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']

class PhoneAuctionForm(forms.Form):
    brand = forms.CharField(max_length=255)
    model = forms.CharField(max_length=255)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    start_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    starting_price = forms.DecimalField(max_digits=10, decimal_places=2)