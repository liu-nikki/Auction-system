from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .forms import PaymentInfoForm, ShippingForm, PhoneAuctionForm, BidForm
from .models import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

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
            phone = auction.phone
            auction.delete()
            phone.delete()
            return render(request, 'success.html', {'auction': auction})  # Pass auction to the template if needed
    else:
        payment_form = PaymentInfoForm(prefix='payment')
        shipping_form = ShippingForm(prefix='shipping')
    return render(request, 'payment_and_shipping.html', {
        'payment_form': payment_form,
        'shipping_form': shipping_form,
        'auction': auction,  # Provide auction to the template to use its details
    })

# Create your views here.
def testmysql(req):
    return render(req, 'home.html')

def phone(request):
    phones = Phone.objects.all()

def login(req):
    return render(req, 'login.html')


def login_view(req):
    if req.method == "POST":
        name = req.POST.get("name", "")
        pwd = req.POST.get("password", "")
        if name and pwd:
            try:
                user = Normaluser.objects.get(username=name)
                print(user.password)
                print(pwd)
                if pwd == user.password:
                    req.session['normal_user_id'] = user.normal_user_id  # Store user ID in session
                    return HttpResponseRedirect(reverse('phone'))  # Use reverse to handle URLs
                else:
                    return HttpResponse("A wrong user name or password.")
            except Normaluser.DoesNotExist:
                return HttpResponse("A wrong user name or password.")
        else:
            return HttpResponse("Please login.")
    else:
        return render(req, 'login.html')  # Show login form

def profile_view(request):
    user_id = request.session.get('normal_user_id')
    if user_id:
        try:
            user = Normaluser.objects.get(normal_user_id=user_id)
            return render(request, 'profile.html', {'user': user})
        except Normaluser.DoesNotExist:
            return HttpResponse("User not found")
    else:
        return redirect('login_view')


def to_register(req):
    return render(req, 'register.html')


def register_view(req):
    name = req.POST.get("name", "")
    pwd = req.POST.get("password", "")
    email = req.POST.get("email", "")
    if name and pwd and email:
        account = Normaluser(username=name, password=pwd, email=email)
        account.save()
        return render(req, 'registration_success.html')
    else:
        return HttpResponse("Please fill all fields.")


def admin_login(req):
    return render(req, 'admin.html')

def admin_view(req):
    name = req.POST.get("name", "")
    pwd = req.POST.get("password", "")
    if name and pwd:
        # check if the credentials match in the database
        c = Adminuser.objects.filter(username=name, password=pwd)
        if c.exists():
            # Redirect to a new view that shows the admin dashboard or user list
            return redirect('list_users')  # Assuming 'list_users' is the name of the view you want to redirect to
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
                return redirect('payment_and_shipping', auction_id=auction.auction_id)  # Adjust this to your actual payment page URL name

    else:
        form = BidForm()
    return render(request, 'dbgroup7_app/bid_page.html', {'auction': auction, 'form': form})

def list_phone_auction_view(request):
    if request.method == 'POST':
        form = PhoneAuctionForm(request.POST)
        if form.is_valid():
            # Create Phone
            phone = Phone(
                brand=form.cleaned_data['brand'],
                model=form.cleaned_data['model'],
                category=form.cleaned_data['category']
            )
            phone.save()

            # Create Auction
            auction = Auction(
                phone=phone,
                start_time=form.cleaned_data['start_time'],
                end_time=form.cleaned_data['end_time'],
                starting_price=form.cleaned_data['starting_price']
            )
            auction.save()

            return redirect('phone')  # Redirect to a success page or the auction detail page
    else:
        form = PhoneAuctionForm()
    return render(request, 'list.html', {'form': form})

# once login in admin
def list_users(request):
    users = Normaluser.objects.all()
    return render(request, 'list_users.html', {'users': users})

def edit_user(request, user_id):
    user = get_object_or_404(Normaluser, pk=user_id)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        # Ensure to hash the password in production using make_password
        user.password = request.POST.get('password')
        user.save()
        return redirect('list_users')
    return render(request, 'edit_user.html', {'user': user})

def delete_user(request, user_id):
    user = get_object_or_404(Normaluser, pk=user_id)
    user.delete()
    return redirect('list_users')

def logout_view(request):
    # logout(request)
    return redirect('login')  # Assumes you have a URL named 'login_view' for your login page