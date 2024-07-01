from django.urls import path, include
from . import views
from accounts import views as acct_views


urlpatterns = [
    path("profile/", views.profileView, name="vendorProfile"),
    path("", acct_views.httpVendorDashboard, name="vendorDashboard"),
    path("menu/", include("menu.urls")),  
]
