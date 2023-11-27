from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from .forms import UserForm
from .models import User, UserProfile
from vendor.forms import VendorForm
from accounts.utils import check_role_customer, check_role_vendor, get_user_role, send_verification_email


# USER REGISTRATION VIEW
def httpRegisterUser(request):
    """
    View for user registration. Validates the form, creates a user, and sends a verification email.
    """
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

             ## SEND VERIFICATION EMAIL
                
            send_verification_email(request, user)
            
            # SHOW A TOAST MESSAGE UPON SUCCESSFUL USER PROFILE CREATION
            messages.success(request, message="Success!, check your email to activate your account.")
            return redirect("registerUser")
        else:
            print("form is invalid")
            print(form.errors)
            
    else:
        form = UserForm()
    
    context = {
        "form": form
    }
    return render(request, "accounts/registerUser.html", context)



# VENDOR REGISTRATION VIEW
def httpRegisterVendor(request):
    """
    View for vendor registration. Validates both user and vendor forms, creates a user, and sends a verification email.
    """
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

            
             ## SEND VERIFICATION EMAIL
            send_verification_email(request, user)

            # HELPER PRINT STATEMENT (REMOVE IN PRODUCTION)
            print(f"{user.first_name} profile is created.")

            # SHOW A TOAST MESSAGE UPON SUCCESSFUL USER PROFILE CREATION
            messages.success(request, message="Success!, check your email to activate your account.")
            return redirect("registerVendor")
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



# ACCOUNT ACCTIVATOR VIEW
def activate(request, uidb64, token):
    """
    Activate user account by setting the 'is_active' status to TRUE.
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None  and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations! Your account is activated")
        return redirect("userAccount")
    else:
        messages.error(request, "invalid activation link")
        return redirect("userAccount")
    

# LOGIN VIEW
def httpLogin(request):
    """
    View for user login. Authenticates the user and redirects to the user's account page.
    """
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect("userAccount")
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
        return redirect("userAccount")    
    return render(request, "accounts/login.html")


# LOGOUT VIEW
def httpLogout(request):
    """
    View for user logout. Logs the user out and redirects to the login page.
    """
    auth.logout(request)
    messages.info(request, "you are logged out")
    return redirect("login")


# USER ACCOUNT MANAGER 
@login_required(login_url='login')
def httpGetUserAccount(request):
    """
    View for managing user accounts. Redirects based on the user's role.
    """
    user = request.user
    redirectUrl = get_user_role(user)
    return redirect(redirectUrl)

# VIEW THAT RESTRICT ACCESS TO ONLY CUSTOMER DASHBOARD
@login_required(login_url='login')
@user_passes_test(check_role_customer)
def httpCustomerDashboard(request):
    """
    View for displaying the customer dashboard. Only accessible to customers.
    """
    return render(request, "accounts/customerDashboard.html")


# VIEW THAT RESTRICT ACCESS TO ONLY VENDOR DASHBOARD
@login_required(login_url='login')
@user_passes_test(check_role_vendor, login_url="login")
def httpVendorDashboard(request):
    """
    View for displaying the vendor dashboard. Only accessible to vendors.
    """
    return render(request, "accounts/vendorDashboard.html")


# RESET PASSWORD VIEW
def httpForgotPassword(request):
    """
    View for resetting user passwords
    """
    pass

def httpResetPasswordValidate(request):
    """
    View for validating user password
    """
    pass

def httpResetPassword(request):
    """
    View for resetting user passwords
    """
    pass
