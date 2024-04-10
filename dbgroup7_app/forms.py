from django import forms
from .models import Paymentinfo, Shipping, Bid

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
