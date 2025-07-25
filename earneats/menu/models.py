from django.db import models
from vendor.models import Vendor
from django.db.models import UniqueConstraint

class Category(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="categories")
    category_name = models.CharField(max_length=50)
    slug = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        constraints = [
            UniqueConstraint(fields=['vendor', 'category_name'], name='unique_vendor_category')
        ]

    def clean(self):
        self.category_name = self.category_name.capitalize()
     
    def __str__(self):
        return self.category_name



class FoodItem(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='fooditems')
    food_title = models.CharField(max_length=50)
    slug = models.CharField(max_length=100)
    description = models.TextField(max_length=255, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='foodimages')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'food'
        verbose_name_plural = 'foods'

    def __str__(self):
        return self.food_title
