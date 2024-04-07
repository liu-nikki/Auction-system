from django.shortcuts import render
# Create your views here.
def testmysql(req):
    return render(req, 'home.html')