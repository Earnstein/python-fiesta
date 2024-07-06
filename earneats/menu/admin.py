from django.contrib import admin
from .models import Category, FoodItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'category_name', 'slug', 'updated_at']
    prepopulated_fields = {'slug': ('category_name', 'vendor')}
    search_fields = ['category_name', 'vendor__vendor_name']
    ordering = ['category_name']


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'food_title', 'slug', 'price', 'category', 'updated_at']
    list_filter = ['is_available']
    prepopulated_fields = {'slug': ('food_title', 'vendor')}
    search_fields = ['food_title', 'description', 'category__category_name']
    ordering = ['food_title', 'price']