from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.text import slugify
from accounts.utils import check_role_vendor
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from menu.models import Category, FoodItem
from menu.forms import CategoryForm
from .forms import VendorForm
from .models import Vendor
from .utils import get_vendor



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
def menuView(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor)
    context = {"categories": categories}
    return render(request, "vendor/menu.html", context)


@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def getMenuByCategory(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    food_items = FoodItem.objects.filter(vendor=vendor, category=category)
    context = {"food_items": food_items, "category": category}
    return render(request, "vendor/getMenuByCategory.html", context)

def createCategory(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data["category_name"]
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            category.save()
            messages.success(request, "Category created successfully")
            return redirect("menu")
    else:
        form = CategoryForm()
    context = {"form": form}
    return render(request, "vendor/createCategory.html", context)

def updateCategory(request, pk=None):
    if request.method == "POST":
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.save()
            messages.success(request, "Category updated successfully")
            return redirect("menu")
    else:
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(instance=category)
    context = {"form": form, "category": category}
    return render(request, "vendor/updateCategory.html", context)

def deleteCategory(request, pk=None):
    category = get_object_or_404(Category, pk=pk)    
    category.delete()
    messages.success(request, "Category deleted successfully")
    return redirect("menu")
        
