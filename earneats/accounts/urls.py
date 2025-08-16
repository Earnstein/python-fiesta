from django.urls import path, include
from . import views

urlpatterns = [

    # USER AUTHENTICATION URLS
    path("registerUser/", views.httpRegisterUser, name="registerUser"),
    path("registerVendor/", views.httpRegisterVendor, name="registerVendor"),
    path("login/", views.httpLogin, name="login"),
    path("logout/", views.httpLogout, name="logout"),

    # USER ACCOUNT URLS
    path("", views.httpGetUserAccount),
    path("myAccount/", views.httpGetUserAccount, name="userAccount"),
    path("customerDashboard/", views.httpCustomerDashboard, name="customerDashboard"),
    path("customerProfile/", views.httpCustomerProfile, name="customerProfile"),
    path("vendorDashboard/", views.httpVendorDashboard, name="vendorDashboard"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),

    # FORGOT PASSWORD AND RESET PASSWORD
    path("forgotPassword/", views.httpForgotPassword, name="forgotPassword"),
    path("resetPasswordValidate/<uidb64>/<token>/", views.httpResetPasswordValidate, name="resetPasswordValidate"),
    path("resetPassword/", views.httpResetPassword, name="resetPassword"),

    path("vendor/", include("vendor.urls")),
]
