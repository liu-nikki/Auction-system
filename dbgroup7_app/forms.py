from django import forms
from .models import Paymentinfo, Shipping

class PaymentInfoForm(forms.ModelForm):
    class Meta:
        model = Paymentinfo
        fields = ['payment_method', 'billing_address']

class ShippingForm(forms.ModelForm):
    class Meta:
        model = Shipping
        fields = ['shipping_address', 'shipping_date']

from django import forms
from .models import Bid

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
