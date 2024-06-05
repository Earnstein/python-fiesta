from django.shortcuts import render, get_object_or_404
from .forms import VendorForm
from .models import Vendor
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from django.contrib import messages
from django.shortcuts import redirect
# Create your views here.

def profileView(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    if request.method != 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
        else:
            messages.error(request, 'Error updating profile')
            print(profile_form.errors, vendor_form.errors)
            return redirect('profile')
            
    profile_form = UserProfileForm(instance=profile)
    vendor_form = VendorForm(instance=vendor)

    context = {'profile_form': profile_form, 'vendor_form': vendor_form, 'profile': profile, 'vendor': vendor}
    return render(request, 'vendor/profile.html', context)



