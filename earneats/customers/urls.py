from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    # USER ACCOUNT URLS
    path("", views.httpGetUserAccount),
    path("myAccount/", views.httpGetUserAccount, name="userAccount"),
    path("dashboard/", views.httpCustomerDashboard, name="dashboard"),
    path("profile/", views.httpCustomerProfile, name="profile"),
    path("settings/", views.customerSettings, name="settings"),
]
