from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

TAILWIND_INPUT = 'w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400 transition'

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': TAILWIND_INPUT,
        'placeholder': 'Email address',
    }), label='Email')
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': TAILWIND_INPUT,
        'placeholder': 'Username',
    }), label='Username')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': TAILWIND_INPUT,
        'placeholder': 'Password',
    }), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': TAILWIND_INPUT,
        'placeholder': 'Confirm password',
    }), label='Confirm password')

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'name': 'username',
        'class': TAILWIND_INPUT,
        'placeholder': 'Username',
    }), label='Username')
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'name': 'password',
        'class': TAILWIND_INPUT,
        'placeholder': 'Password',
    }), label='Password')

    class Meta:
        model = User
        fields = ('username', 'password')