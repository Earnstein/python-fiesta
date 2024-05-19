from django.urls import path
from . import views

urlpatterns = [
    path("registerUser/", views.httpRegisterUser, name="registerUser"),
    path("registerVendor/", views.httpRegisterVendor, name="registerVendor"),
    path("login/", views.httpLogin, name="login"),
    path("logout/", views.httpLogout, name="logout"),
    path("", views.httpGetUserAccount),
    path("myAccount/", views.httpGetUserAccount, name="userAccount"),
    path("customerDashboard/", views.httpCustomerDashboard, name="customerDashboard"),
    path("vendorDashboard/", views.httpVendorDashboard, name="vendorDashboard"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("forgotPassword/", views.httpForgotPassword, name="forgotPassword"),
    path("resetPasswordValidate/<uidb64>/<token>/", views.httpResetPasswordValidate, name="resetPasswordValidate"),
    path("resetPassword/", views.httpResetPassword, name="resetPassword"),
]
