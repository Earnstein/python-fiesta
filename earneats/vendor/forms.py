from django import forms
from .models import Vendor
from accounts.form_validations import allow_images_only

class VendorForm(forms.ModelForm):
    vendor_license = forms.FileField(widget=forms.FileInput(attrs={"class": "btn btn-info"}), validators=[allow_images_only])
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']
    