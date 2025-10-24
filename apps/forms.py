from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, EmailField
from django.forms.forms import Form
from django.forms.widgets import PasswordInput, EmailInput, TextInput
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
from apps.models import CustomUser


class SignUpForm(ModelForm):
    confirm_password = CharField(
        max_length=255,
        required=True,
        widget=PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Confirm Password'})
    )
    password = CharField(
        max_length=255,
        required=True,
        widget=PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter Password'})
    )
    email = EmailField(
        required=True,
        widget=EmailInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter your email'})
    )
    first_name = CharField(
        required=True,
        widget=TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter your name'})
    )
    company = CharField(
        required=False,
        widget=TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter your company name'})
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'email', 'password', 'company']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError("Passwords don't match")

        # Hash the password before saving
        cleaned_data['password'] = make_password(password)

        return cleaned_data



class LoginForm(Form):
    email = EmailField(
        required=True,
        widget=EmailInput(attrs={
            'class': 'form-control input-lg',
            'placeholder': 'Email',
            'autocomplete': 'email',
        })
    )
    password = CharField(
        required=True,
        max_length=128,
        widget=PasswordInput(attrs={
            'class': 'form-control input-lg',
            'placeholder': 'Password',
            'autocomplete': 'current-password',
        })
    )

    def __init__(self, *args, request=None, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get('email')
        password = cleaned.get('password')

        if not email or not password:
            return cleaned

        user = None
        if self.request is not None:
            user = authenticate(request=self.request, email=email, password=password)

        if user is None:
            user = authenticate(username=email, password=password)

        if user is None:
            raise ValidationError("Incorrect email or password")

        self.user = user
        return cleaned







class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'phone_number', 'mobile_number',
            'email', 'skype', 'pfp_url',
            'facebook_url', 'twitter_url', 'linkedin_url'
        ]
        widgets = {
            'pfp_url': forms.FileInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'skype': forms.TextInput(attrs={'class': 'form-control'}),
            'facebook_url': forms.TextInput(attrs={'class': 'form-control'}),
            'twitter_url': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin_url': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
