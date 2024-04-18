from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .forms import PaymentInfoForm, ShippingForm, PhoneAuctionForm, BidForm
from .models import *
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
        'auction': auction,
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
            return redirect('list_users')
        else:
            return HttpResponse("A wrong admin user name or password.")
    else:
        return HttpResponse("Please login.")


def phone(request):
    phones = Phone.objects.all()
    for phone in phones:
        auction = Auction.objects.filter(phone=phone).first()
        if auction:
            highest_bid = Bid.objects.filter(auction=auction).order_by('-amount').first()
            # If there's a highest bid, set current_price to the highest bid amount
            if highest_bid:
                phone.current_price = highest_bid.amount
            else:
                # Otherwise, set current_price to the starting price of the auction
                phone.current_price = auction.starting_price
            phone.auction_id = auction.auction_id

    return render(request, 'phone.html', {'phones': phones})


def bid_view(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)
    highest_bid = Bid.objects.filter(auction=auction).order_by('-amount').first()
    
    current_highest_bid = highest_bid.amount if highest_bid else auction.starting_price

    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            new_bid_amount = form.cleaned_data['amount']

            # Check if the new bid amount is more than $500 higher than the highest bid
            if new_bid_amount > current_highest_bid + 500:
                bid = form.save(commit=False)
                bid.auction = auction
                normal_user_instance = get_object_or_404(Normaluser, pk=1)  # Assuming static user, adjust as needed
                bid.normal_user = normal_user_instance
                bid.save()
                return redirect('payment_and_shipping', auction_id=auction.auction_id)
            else:
                # Save the bid in all cases
                bid = form.save(commit=False)
                bid.auction = auction
                normal_user_instance = get_object_or_404(Normaluser, pk=1)  # Assuming static user, adjust as needed
                bid.normal_user = normal_user_instance
                bid.save()
                return redirect('phone')

    else:
        form = BidForm()
    return render(request, 'dbgroup7_app/bid_page.html', {
        'auction': auction,
        'form': form,
        'current_highest_bid': current_highest_bid  # Passing the highest bid to the template
    })

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
    return redirect('login')