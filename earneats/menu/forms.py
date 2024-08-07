from django import forms
from .models import Category, FoodItem
from accounts.form_validations import allow_images_only

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']

class FoodItemForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={"class": "btn btn-info"}), validators=[allow_images_only])
    class Meta:
        model = FoodItem
        fields = ['food_title', 'category', 'description', 'price', 'image', 'is_available' ]
    
    def __init__(self, *args, **kwargs):
        vendor = kwargs.pop('vendor', None)
        super(FoodItemForm, self).__init__(*args, **kwargs)
        if vendor:
            self.fields['category'].queryset =  Category.objects.filter(vendor=vendor)
