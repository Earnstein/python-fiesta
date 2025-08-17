from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from accounts.utils import check_role_customer, get_user_role
from accounts.forms import UserProfileForm, UserSettingsForm
from accounts.models import UserProfile
from vendor.models import Vendor
from earneats.utils import get_location_from_request


@login_required(login_url='login')
def httpGetUserAccount(request):
    """
    View for managing user accounts. Redirects based on the user's role.
    """
    user = request.user
    redirectUrl = get_user_role(user)
    return redirect(redirectUrl)


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def httpCustomerDashboard(request):
    """
    View for displaying the customer dashboard. Only accessible to customers.
    """
    location = get_location_from_request(request)
    page_number = request.GET.get("page", 1)
    vendors_per_page = 5
    
    # Get vendors with opening status
    vendor_queryset = (
        Vendor.approved
        .with_opening_status()
        .select_related('user', 'user_profile')
        .prefetch_related('opening_hours', 'categories')
    )
    
    if location:
        lat, lng = location
        user_location = Point(lng, lat, srid=4326)
        vendor_queryset = vendor_queryset.annotate(
            distance=Distance("user_profile__location", user_location)
        ).order_by('distance', 'vendor_name')
    else:
        vendor_queryset = vendor_queryset.order_by('vendor_name')
    
    # Paginate the queryset
    paginator = Paginator(vendor_queryset, vendors_per_page)
    
    try:
        vendors = paginator.page(page_number)
    except (EmptyPage, PageNotAnInteger):
        vendors = paginator.page(1)
    
    context = {
        "vendors": vendors,
        "current_day": timezone.now().isoweekday(),
        "total_vendors": paginator.count,
        "has_location": bool(location)
    }
    return render(request, "customers/customerDashboard.html", context)


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def httpCustomerProfile(request):
    """
    View for displaying and updating customer profile. Only accessible to customers.
    """
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == "POST":
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("customerProfile")
        else:
            messages.error(request, "Error updating profile")
            print(profile_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
    
    context = {
        "profile_form": profile_form,
        "profile": profile,
    }
    return render(request, "customers/customerProfile.html", context)


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerSettings(request):
    """
    View for updating customer basic information (firstname, lastname, username, phone_number).
    Only accessible to customers.
    """
    if request.method == "POST":
        settings_form = UserSettingsForm(request.POST, instance=request.user)
        if settings_form.is_valid():
            settings_form.save()
            messages.success(request, "Settings updated successfully")
            return redirect("customerSettings")
        else:
            messages.error(request, "Error updating settings")
            print(settings_form.errors)
    else:
        settings_form = UserSettingsForm(instance=request.user)
    
    context = {
        "settings_form": settings_form,
    }
    return render(request, "customers/customerSettings.html", context)
