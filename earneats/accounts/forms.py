from django import forms
from .models import User, UserProfile
from .form_validations import allow_images_only
from phonenumber_field.formfields import PhoneNumberField
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}))
    
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add autocomplete attributes for better browser autofill
        self.fields['first_name'].widget.attrs.update({
            'autocomplete': 'given-name',
            'placeholder': 'Enter your first name'
        })
        self.fields['last_name'].widget.attrs.update({
            'autocomplete': 'family-name',
            'placeholder': 'Enter your last name'
        })
        self.fields['username'].widget.attrs.update({
            'autocomplete': 'username',
            'placeholder': 'Enter your username'
        })
        self.fields['email'].widget.attrs.update({
            'autocomplete': 'email',
            'placeholder': 'Enter your email'
        })
    
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match"
            )
    

class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Your address...", "required": "required"}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={"class": "btn btn-info"}), validators=[allow_images_only])
    cover_picture = forms.FileField(widget=forms.FileInput(attrs={"class": "btn btn-info"}), validators=[allow_images_only])
    latitude = forms.CharField(widget=forms.TextInput())
    longitude = forms.CharField(widget=forms.TextInput())
    class Meta:
        model = UserProfile
        fields = ["profile_picture", "cover_picture",  "address", "city", "state", "country", "pin_code", "latitude", "longitude"]


class UserSettingsForm(forms.ModelForm):
    """Form for updating basic user information (firstname, lastname, username, phone_number)"""
    phone_number = PhoneNumberField()
    
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "phone_number"]
        

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            # Check if username exists for other users
            if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("This username is already taken.")
        return username
