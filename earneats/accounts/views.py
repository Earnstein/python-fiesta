from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages
from vendor.forms import VendorForm
# Create your views here.

def httpRegisterUser(request):
    if request.method == "POST":
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
    if request.method == "POST":
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
    return render(request, "accounts/registerVendor.html", context )