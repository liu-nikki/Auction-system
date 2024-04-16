"""
URL configuration for dbgroup7 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from dbgroup7_app import views
from django.contrib import admin
from django.urls import path, include
from dbgroup7_app import views
from dbgroup7_app.views import bid_view, testmysql

urlpatterns = [
    path('', views.login),
    path('toregister/', views.to_register),
    path("register/", views.register_view),
    path('admin/', views.admin_login),
    path('admin/admin_view/', views.admin_view, name="admin_view"),
    path('phone/', views.phone, name='phone'),
    path('login/', views.login_view, name='login'),
    path('payment-and-shipping/<int:auction_id>/', views.payment_and_shipping_view, name='payment_and_shipping'),
    path('auction/<int:auction_id>/bid/', bid_view, name='bid_view'),
    path('list/', views.list_phone_auction_view, name='list_phone_auction'),
]
