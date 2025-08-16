from django import forms
from django.forms import widgets
from .models import Vendor, OpeningHours
from accounts.form_validations import allow_images_only

class VendorForm(forms.ModelForm):
    vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_images_only])

    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']

class OpeningHoursForm(forms.ModelForm):
    """Form for OpeningHours with 12-hour time format."""
    
    class Meta:
        model = OpeningHours
        fields = ['day_of_week', 'from_hour', 'to_hour', 'is_open']
        widgets = {
            'day_of_week': forms.Select(attrs={'class': 'form-control'}),
            'from_hour': forms.TimeInput(
                format='%H:%M',
                attrs={
                    'type': 'time',
                    'class': 'form-control',
                    'placeholder': '09:00'
                }
            ),
            'to_hour': forms.TimeInput(
                format='%H:%M',
                attrs={
                    'type': 'time',
                    'class': 'form-control',
                    'placeholder': '17:00'
                }
            ),
            'is_open': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        vendor = kwargs.pop('vendor', None)
        super().__init__(*args, **kwargs)
        
        if vendor:
            # Get existing days for this vendor
            existing_days = vendor.opening_hours.values_list('day_of_week', flat=True)
            
            # Filter out already configured days from choices
            day_choices = list(self.fields['day_of_week'].choices)
            available_choices = [(day_num, day_name) for day_num, day_name in day_choices if day_num not in existing_days]
            
            # Add a placeholder option
            if available_choices:
                self.fields['day_of_week'].choices = [('', '-- Select a day --')] + available_choices
            else:
                self.fields['day_of_week'].choices = [('', 'All days are already configured')]
                self.fields['day_of_week'].widget.attrs['disabled'] = 'disabled'
    
    def clean(self):
        """Validate the entire form."""
        cleaned_data = super().clean()
        from_hour = cleaned_data.get('from_hour')
        to_hour = cleaned_data.get('to_hour')
        is_open = cleaned_data.get('is_open')
        
        # If day is marked as open, both times are required
        if is_open:
            if not from_hour:
                self.add_error('from_hour', 'Opening time is required when day is marked as open.')
            if not to_hour:
                self.add_error('to_hour', 'Closing time is required when day is marked as open.')
            
            # Validate time order
            if from_hour and to_hour and from_hour >= to_hour:
                self.add_error('to_hour', 'Closing time must be after opening time.')
        
        return cleaned_data
    