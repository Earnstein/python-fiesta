from django.shortcuts import render, get_object_or_404
from .forms import VendorForm
from .models import Vendor
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.utils import check_role_vendor

@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def profileView(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    if request.method == "POST":
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("vendorProfile")
        else:
            messages.error(request, "Error updating profile")
            print(profile_form.errors, vendor_form.errors)
    else:    
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)

    context = {"profile_form": profile_form, "vendor_form": vendor_form, "profile": profile, "vendor": vendor}
    return render(request, "vendor/profile.html", context)



