from django.urls import path
from . import views

urlpatterns = [
    # USER ACCOUNT URLS
    path("", views.httpGetUserAccount),
    path("myAccount/", views.httpGetUserAccount, name="userAccount"),
    path("customerDashboard/", views.httpCustomerDashboard, name="customerDashboard"),
    path("customerProfile/", views.httpCustomerProfile, name="customerProfile"),
    path("customerSettings/", views.customerSettings, name="customerSettings"),
]
