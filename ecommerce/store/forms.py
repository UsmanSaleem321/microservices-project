from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Enter a valid email address.")
    class Meta:
        model  = User
        fields = ('first_name','last_name','username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with that email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model  = ShippingAddress
        fields = '__all__'

class ProdcutForm(forms.ModelForm):
    class Meta:
        model  = Product
        fields = '__all__'
        exclude = ['seller']