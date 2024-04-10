from django.shortcuts import render, HttpResponse
from .forms import PaymentInfoForm, ShippingForm
from .models import *
# Create your views here.
# def home(request):
#     return HttpResponse("Welcome to My Site!")

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
    return render(request, 'phone.html', {'phones': phones})
