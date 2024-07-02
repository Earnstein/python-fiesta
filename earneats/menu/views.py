from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.text import slugify
from accounts.utils import check_role_vendor
from menu.models import Category, FoodItem
from menu.forms import CategoryForm, FoodItemForm
from vendor.utils import get_vendor


@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def menuView(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor)
    context = {"categories": categories}
    return render(request, "vendor/menu.html", context)


@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def getCategory(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    food_items = FoodItem.objects.filter(vendor=vendor, category=category)
    context = {"food_items": food_items, "category": category}
    return render(request, "vendor/category/getCategory.html", context)


@login_required(login_url="login")
@user_passes_test(check_role_vendor)
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
    return render(request, "vendor/category/createCategory.html", context)


@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def updateCategory(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category.save()
            messages.success(request, "Category updated successfully")
            return redirect("menu")
    else:
        form = CategoryForm(instance=category)
    context = {"form": form, "category": category}
    return render(request, "vendor/category/updateCategory.html", context)



@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def deleteCategory(request, pk=None):
    category = get_object_or_404(Category, pk=pk)    
    category.delete()
    messages.success(request, "Category deleted successfully")
    return redirect("menu")
        


@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def createFood(request):
    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food_form = form.save(commit=False)
            food_form.vendor = get_vendor(request)
            food_form.slug = slugify(food_title)
            food_form.save()
            messages.success(request, "Food was added successfully")
            return redirect("menu")
    form = FoodItemForm()
    context = {"form": form}
    return render(request, "vendor/food/createFood.html", context)


@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def updateFood(request, pk=None):
    food_item = get_object_or_404(FoodItem, pk=pk)
    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES, instance=food_item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item was updated successfully")
            return redirect("menu")
        else:
            print(form.errors)
    form = FoodItemForm(instance=food_item)
    context = { "form": form,"food_item": food_item }
    return render(request, "vendor/food/updateFood.html", context)


@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def deleteFood(request, pk=None):
    food_item = get_object_or_404(FoodItem, pk=pk)
    food_item.delete()
    messages.success(request, f"{food_item.food_title} is succussfully deleted.")
    return redirect("menu")