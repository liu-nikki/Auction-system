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
    path('', views.login, name='login'),
    # path('toregister/', views.to_register),
    path('toregister/', views.to_register, name='toregister'),  # Ensure the name is specified
    path("register/", views.register_view),
    path('admin/', views.admin_login),
    path('admin/admin_view/', views.admin_view, name="admin_view"),
    path('phone/', views.phone, name='phone'),
    path('login/', views.login_view, name='login'),
    path('payment-and-shipping/<int:auction_id>/', views.payment_and_shipping_view, name='payment_and_shipping'),
    path('auction/<int:auction_id>/bid/', bid_view, name='bid_view'),
    path('list/', views.list_phone_auction_view, name='list_phone_auction'),
    path('profile/', views.profile_view, name='profile_view'),
    # Adding User Management URLs
    path('admin/users/', views.list_users, name='list_users'),
    path('admin/users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('admin/users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('logout/', views.logout_view, name='logout'),
]

