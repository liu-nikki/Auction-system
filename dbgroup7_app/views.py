from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .forms import PaymentInfoForm, ShippingForm, BidForm
from .models import *
from django.contrib import messages

def payment_and_shipping_view(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)  # Ensure you have the auction
    if request.method == 'POST':
        payment_form = PaymentInfoForm(request.POST, prefix='payment')
        shipping_form = ShippingForm(request.POST, prefix='shipping')
        if payment_form.is_valid() and shipping_form.is_valid():
            payment_info = payment_form.save(commit=False)
            shipping_info = shipping_form.save(commit=False)
            # Assume you have a field in PaymentInfo and Shipping models to link them to an auction
            payment_info.auction = auction
            shipping_info.auction = auction
            payment_info.save()
            shipping_info.save()
            return render(request, 'success.html', {'auction': auction})  # Pass auction to the template if needed
    else:
        payment_form = PaymentInfoForm(prefix='payment')
        shipping_form = ShippingForm(prefix='shipping')
    return render(request, 'payment_and_shipping.html', {
        'payment_form': payment_form,
        'shipping_form': shipping_form,
        'auction': auction,  # Provide auction to the template to use its details
    })

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from .models import Auction, Bid, Normaluser
from .forms import BidForm

# Create your views here.
def testmysql(req):
    return render(req, 'home.html')


# def phone(req):
#     return render(req, 'phone.html')

def phone(request):
    phones = Phone.objects.all()


def login(req):
    return render(req, 'login.html')


# after login 
def login_view(req):
    name = req.POST.get("name", "")
    pwd = req.POST.get("password", "")
    if name and pwd:
        # see if match database 
        c = Normaluser.objects.filter(username=name, password=pwd)
        if c.exists():
            return HttpResponse("Login Successfully!")
        else:
            return HttpResponse("A wrong user name or password.")
    else:
        return HttpResponse("Please login.")
    # return render(req, 'login_view.html')


def to_register(req):
    return render(req, 'register.html')


def register_view(req):
    name = req.POST.get("name", "")
    pwd = req.POST.get("password", "")
    email = req.POST.get("email", "")
    if name and pwd and email:
        account = Normaluser(username=name, password=pwd, email=email)
        account.save()
        return HttpResponse("Register Successfully!")
    else:
        return HttpResponse("Please register.")


def admin_login(req):
    return render(req, 'admin.html')


def admin_view(req):
    name = req.POST.get("name", "")
    pwd = req.POST.get("password", "")
    if name and pwd:
        # see if match database 
        c = Adminuser.objects.filter(username=name, password=pwd)
        if c.exists():
            return HttpResponse("Admin Login Successfully!")
        else:
            return HttpResponse("A wrong admin user name or password.")
    else:
        return HttpResponse("Please login.")


def phone(request):
    phones = Phone.objects.all()
    for phone in phones:
        auction = Auction.objects.filter(phone_id=phone.phone_id).first()
        if auction:
            phone.current_price = auction.starting_price
            phone.auction_id = auction.auction_id
    return render(request, 'phone.html', {'phones': phones})


def bid_view(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            new_bid_amount = form.cleaned_data['amount']
            highest_bid = Bid.objects.filter(auction=auction).order_by('-amount').first()

            if highest_bid is None:
                highest_bid_amount = auction.starting_price
            else:
                highest_bid_amount = highest_bid.amount

            if new_bid_amount <= highest_bid_amount + 50:
                messages.error(request, "Bidding Failed, higher bid price exist, please try again later.")
            else:
                bid = form.save(commit=False)
                bid.auction = auction
                normal_user_instance = get_object_or_404(Normaluser, pk=1)
                bid.normal_user = normal_user_instance
                bid.save()
                messages.success(request, "Bid successfully placed! Proceed to payment.")
                return redirect('payment_and_shipping', auction_id=auction.auction_id)  # Adjust this to your actual payment page URL name

    else:
        form = BidForm()

    return render(request, 'dbgroup7_app/bid_page.html', {'auction': auction, 'form': form})
