from django.urls import path
from . import views

urlpatterns = [
    path("registerUser/", views.httpRegisterUser, name="registerUser"),
    path("registerVendor/", views.httpRegisterVendor, name="registerVendor"),
    path("login/", views.httpLogin, name="login"),
    path("logout/", views.httpLogout, name="logout"),
    path("myAccount/", views.httpGetUserAccount, name="myAccount"),
    path("customerDashboard/", views.httpCustomerDashboard, name="customerDashboard"),
    path("vendorDashboard/", views.httpVendorDashboard, name="vendorDashboard"),
]
