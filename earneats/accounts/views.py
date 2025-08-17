from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.text import slugify
from .forms import UserForm, UserProfileForm, UserSettingsForm
from .models import User, UserProfile
from vendor.forms import VendorForm
from accounts.utils import check_role_customer, check_role_vendor, get_user_role, send_custom_email
from vendor.models import Vendor

# USER REGISTRATION VIEW
def httpRegisterUser(request):
    """
    View for user registration. Validates the form, creates a user, and sends a verification email.
    """
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect("userAccount")
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
                
            send_custom_email(request, user, email_type='verification')
            
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
            vendor_name = vendorForm.cleaned_data["vendor_name"]
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.vendor_slug = slugify(f"{vendor_name}-{str(user.id)}")
            vendor.save()

            
             ## SEND VERIFICATION EMAIL
            send_custom_email(request, user, email_type='verification')

            # TODO: HELPER PRINT STATEMENT (REMOVE IN PRODUCTION)
            print(f"{user.first_name} profile is created.")

            # SHOW A TOAST MESSAGE UPON SUCCESSFUL USER PROFILE CREATION
            messages.success(request, message="Success!... check your email to activate your account.")
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
    
    if user is None and not default_token_generator.check_token(user, token):
        messages.error(request, "invalid activation link")
        return redirect("userAccount")
    
    user.is_active = True
    user.save()
    messages.success(request, "Congratulations! Your account is activated")
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


# FORGET PASSWORD VIEW
def httpForgotPassword(request):
    """
    View for resetting user passwords
    """
    if request.method == "POST":
        email = request.POST['email']
        is_user = User.objects.filter(email=email).exists()
        if not is_user:
            messages.error(request, "account does not exists")
            return redirect("login")
        
        #send reset password email
        user = User.objects.get(email__exact=email)
        send_custom_email(request, user, email_type="password_reset")
        messages.success(request, "A reset link has been sent to your email")
        return redirect("login")

    return render(request, "accounts/forgotPassword.html")

# RESET PASSWORD VIEW
def httpResetPasswordValidate(request, uidb64, token):
    """
    View for validating user password
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is None and not default_token_generator.check_token(user, token):
        messages.error(request, "This link has expired")
        return redirect("userAccount")
    
    request.session['uid'] = uid
    messages.info(request, "Please reset your password")
    return redirect("resetPassword")
 
 # RESET PASSWORD VIEW
def httpResetPassword(request):
    """
    View for resetting user passwords
    """
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if password != confirm_password:
            messages.error(request, "passwords do not match!")
            return redirect("resetPassword")
        pk = request.session.get('uid')
        user = User.objects.get(pk=pk)
        user.set_password(password)
        user.is_active = True
        user.save()
        messages.success(request, "Password reset successful")
         
        return redirect('login')
    return render(request, "accounts/resetPassword.html")
