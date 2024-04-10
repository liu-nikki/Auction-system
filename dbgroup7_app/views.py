from django.shortcuts import render, HttpResponse
from .forms import PaymentInfoForm, ShippingForm
# Create your views here.
def home(request):
    return HttpResponse("Welcome to My Site!")

def payment_and_shipping_view(request):
    if request.method == 'POST':
        payment_form = PaymentInfoForm(request.POST, prefix='payment')
        shipping_form = ShippingForm(request.POST, prefix='shipping')
        if payment_form.is_valid() and shipping_form.is_valid():
            payment_form.save()
            shipping_form.save()
            return render(request, 'success.html')  # You need to create a success.html template
    else:
        payment_form = PaymentInfoForm(prefix='payment')
        shipping_form = ShippingForm(prefix='shipping')
    return render(request, 'payment_and_shipping.html', {
        'payment_form': payment_form,
        'shipping_form': shipping_form,
    })