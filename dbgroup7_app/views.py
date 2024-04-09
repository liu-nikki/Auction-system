from django.shortcuts import render
from django.http import HttpResponse
from .models import *


# Create your views here.
def testmysql(req):
    return render(req, 'home.html')


# def phone(req):
#     return render(req, 'phone.html')

def phone(request):
    phones = Phone.objects.all()
    return render(request, 'phone.html', {'phones': phones})
