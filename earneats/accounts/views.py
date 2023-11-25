from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages, auth
from vendor.forms import VendorForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from accounts.utils import getUserRole
# Create your views here.

# Restrict the vendor from accessing customer page and vice versa.

def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied



def httpRegisterUser(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect("dashboard")
    elif request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            print(f"{user.first_name} profile is created.")
            # Show a toast message upon successful user profile creation
            messages.success(request, message="Your account has been successfully registered!")
            redirect("registerUser")
        else:
            print("form is invalid")
            print(form.errors)
            
    else:
        form = UserForm()
    context = {
        "form": form
    }
    return render(request, "accounts/registerUser.html", context)


def httpRegisterVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect("vendorDashboard")
    elif request.method == "POST":
        form = UserForm(request.POST)
        vendorForm = VendorForm(request.POST, request.FILES)
        if form.is_valid() and vendorForm.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()
            vendor = vendorForm.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            print(f"{user.first_name} profile is created.")
            # Show a toast message upon successful user profile creation
            messages.success(request, message="Your account has been successfully registered! Please wait for approval.")
            redirect("registerVendor")
        else:
            print("Invalid vendor form")
            print(form.errors)

    else:
        form = UserForm()
        vendorForm = VendorForm()

    context = {
        "form": form,
        "v_form": vendorForm
    }
    return render(request, "accounts/registerVendor.html", context)


def httpLogin(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect("myAccount")
    elif request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        email = email.lower()
        user = auth.authenticate(email=email, password=password)
        
        if user is None:
            messages.error(request, "Invalid login credentials")
            return redirect("login")
        
        auth.login(request, user)
        messages.success(request, "You are logged in")
        return redirect("myAccount")    
    return render(request, "accounts/login.html")

def httpLogout(request):
    auth.logout(request)
    messages.info(request, "you are logged out")
    return redirect("login")



@login_required(login_url='login')
def httpGetUserAccount(request):
    user = request.user
    redirectUrl = getUserRole(user)
    return redirect(redirectUrl)


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def httpCustomerDashboard(request):
    return render(request, "accounts/customerDashboard.html")


@login_required(login_url='login')
@user_passes_test(check_role_vendor, login_url="login")
def httpVendorDashboard(request):
    return render(request, "accounts/vendorDashboard.html")
