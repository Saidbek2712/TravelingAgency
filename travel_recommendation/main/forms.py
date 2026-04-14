"""
Forms for user registration and recommendation preferences.
Uses dynamic choices from Category and BudgetCategory models.
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Category, BudgetCategory


class RegistrationForm(UserCreationForm):
    """Extended registration form with email field."""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'glass-input',
            'placeholder': 'Email address',
            'autocomplete': 'email',
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'username': 'Username',
            'password1': 'Password',
            'password2': 'Confirm password',
        }
        for field_name, field in self.fields.items():
            field.widget.attrs.setdefault('class', 'glass-input')
            if field_name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[field_name]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """Simple login form."""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'glass-input',
            'placeholder': 'Username',
            'autocomplete': 'username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'glass-input',
            'placeholder': 'Password',
            'autocomplete': 'current-password',
        })
    )


class RecommendationForm(forms.Form):
    """Form for budget and preference selection — choices from DB."""
    budget = forms.ModelChoiceField(
        queryset=BudgetCategory.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'glass-radio'}),
        label='Your Budget Range',
        empty_label=None,
    )
    preferences = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'glass-checkbox'}),
        label='What do you love?',
        help_text='Select one or more preferences',
    )
