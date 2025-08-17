from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.utils import check_role_vendor
from accounts.forms import UserProfileForm, UserSettingsForm
from accounts.models import UserProfile
from .forms import VendorForm
from .models import Vendor
from django.http import JsonResponse
from django.utils import timezone
from .models import Vendor, OpeningHours, DAY_OF_WEEK_CHOICES
from .forms import OpeningHoursForm
from datetime import time
from django.db import IntegrityError
from accounts.context_processors import get_vendor


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


@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def opening_hours_list(request):
    """List all opening hours for the logged-in vendor."""
    vendor = get_object_or_404(Vendor, user=request.user)
    opening_hours = vendor.get_all_opening_hours()
    
    # Calculate available days (days not yet configured)
    configured_days = set(opening_hours.values_list('day_of_week', flat=True))
    available_days = [(day_num, day_name) for day_num, day_name in DAY_OF_WEEK_CHOICES if day_num not in configured_days]
    available_days_count = len(available_days)
    
    # Get current day for real-time status
    current_day = timezone.now().isoweekday()
    
    # Check if any opening hours are currently open
    currently_open = any(hours.is_currently_open() for hours in opening_hours)
    
    context = {
        'vendor': vendor,
        'opening_hours': opening_hours,
        'day_choices': DAY_OF_WEEK_CHOICES,
        'available_days': available_days,
        'available_days_count': available_days_count,
        'current_day': current_day,
        'currently_open': currently_open,
    }
    return render(request, 'vendor/opening_hours/list.html', context)

@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def opening_hours_create(request):
    """Create new opening hours."""
    vendor = get_object_or_404(Vendor, user=request.user)
    
    if request.method == 'POST':
        form = OpeningHoursForm(request.POST, vendor=vendor)
        if form.is_valid():
            # Check if opening hours already exist for this day
            day_of_week = form.cleaned_data['day_of_week']
            existing_hours = vendor.opening_hours.filter(day_of_week=day_of_week).first()
            
            if existing_hours:
                messages.error(request, f'Opening hours for {dict(DAY_OF_WEEK_CHOICES)[day_of_week]} already exist. Please edit the existing entry instead.')
                return redirect('opening_hours_list')
            
            try:
                opening_hours = form.save(commit=False)
                opening_hours.vendor = vendor
                opening_hours.save()
                messages.success(request, f'Opening hours for {opening_hours.get_day_name()} created successfully!')
                return redirect('opening_hours_list')
            except IntegrityError:
                messages.error(request, f'Opening hours for {dict(DAY_OF_WEEK_CHOICES)[day_of_week]} already exist. Please edit the existing entry instead.')
                return redirect('opening_hours_list')
    else:
        form = OpeningHoursForm(vendor=vendor)
    
    context = {
        'vendor': vendor,
        'form': form,
        'action': 'Create',
    }
    return render(request, 'vendor/opening_hours/form.html', context)

@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def opening_hours_edit(request, pk):
    """Edit existing opening hours."""
    vendor = get_object_or_404(Vendor, user=request.user)
    opening_hours = get_object_or_404(OpeningHours, pk=pk, vendor=vendor)
    
    if request.method == 'POST':
        form = OpeningHoursForm(request.POST, instance=opening_hours)
        if form.is_valid():
            form.save()
            messages.success(request, f'Opening hours for {opening_hours.get_day_name()} updated successfully!')
            return redirect('opening_hours_list')
    else:
        form = OpeningHoursForm(instance=opening_hours)
    
    context = {
        'vendor': vendor,
        'form': form,
        'opening_hours': opening_hours,
        'action': 'Edit',
    }
    return render(request, 'vendor/opening_hours/form.html', context)

@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def opening_hours_delete(request, pk):
    """Delete opening hours."""
    vendor = get_object_or_404(Vendor, user=request.user)
    opening_hours = get_object_or_404(OpeningHours, pk=pk, vendor=vendor)
    
    if request.method == 'POST':
        day_name = opening_hours.get_day_name()
        opening_hours.delete()
        messages.success(request, f'Opening hours for {day_name} deleted successfully!')
        return redirect('opening_hours_list')
    
    context = {
        'vendor': vendor,
        'opening_hours': opening_hours,
    }
    return render(request, 'vendor/opening_hours/delete.html', context)

@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def opening_hours_bulk_edit(request):
    """Bulk edit opening hours for the entire week."""
    vendor = get_object_or_404(Vendor, user=request.user)
    
    if request.method == 'POST':
        # Process form data for all days Monday - 1 to Sunday - 7
        for day_num in range(1, 8):
            is_open = request.POST.get(f'is_open_{day_num}') == 'on'
            from_hour_str = request.POST.get(f'from_hour_{day_num}')
            to_hour_str = request.POST.get(f'to_hour_{day_num}')
            
            # Get or create opening hours for this day
            opening_hours, created = OpeningHours.objects.get_or_create(
                vendor=vendor,
                day_of_week=day_num,
                defaults={
                    'from_hour': time(9, 0),
                    'to_hour': time(17, 0),
                    'is_open': is_open
                }
            )
            
            if is_open and from_hour_str and to_hour_str:
                try:
                    from_hour = time.fromisoformat(from_hour_str)
                    to_hour = time.fromisoformat(to_hour_str)
                    opening_hours.from_hour = from_hour
                    opening_hours.to_hour = to_hour
                    opening_hours.is_open = True
                except ValueError:
                    messages.error(request, f'Invalid time format for {dict(DAY_OF_WEEK_CHOICES)[day_num]}')
                    continue
            else:
                opening_hours.is_open = False
                opening_hours.from_hour = time(0, 0)
                opening_hours.to_hour = time(0, 0)
            
            opening_hours.save()
        
        messages.success(request, 'Opening hours updated successfully!')
        return redirect('opening_hours_list')
    
    # Get existing opening hours for the week
    opening_hours_dict = {}
    for hours in vendor.get_all_opening_hours():
        opening_hours_dict[hours.day_of_week] = hours
    
    # Ensure all days have entries (for consistent display)
    for day_num in range(1, 8):
        if day_num not in opening_hours_dict:
            # Create a placeholder entry for display purposes
            opening_hours_dict[day_num] = type('obj', (object,), {
                'day_of_week': day_num,
                'is_open': False,
                'from_hour': time(9, 0),
                'to_hour': time(17, 0)
            })()
    
    context = {
        'vendor': vendor,
        'opening_hours_dict': opening_hours_dict,
        'day_choices': DAY_OF_WEEK_CHOICES,
    }
    return render(request, 'vendor/opening_hours/bulk_edit.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor, login_url="login")
def httpVendorDashboard(request):
    """
    View for displaying the vendor dashboard. Only accessible to vendors.
    """
    context = get_vendor(request)
    return render(request, "vendor/vendorDashboard.html", context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorSettings(request):
    """
    View for updating vendor basic information (firstname, lastname, username, phone_number).
    Only accessible to vendors.
    """
    if request.method == "POST":
        settings_form = UserSettingsForm(request.POST, instance=request.user)
        if settings_form.is_valid():
            settings_form.save()
            messages.success(request, "Settings updated successfully")
            return redirect("vendorSettings")
        else:
            messages.error(request, "Error updating settings")
            print(settings_form.errors)
    else:
        settings_form = UserSettingsForm(instance=request.user)
    
    context = {
        "settings_form": settings_form,
    }
    return render(request, "vendor/vendorSettings.html", context)
