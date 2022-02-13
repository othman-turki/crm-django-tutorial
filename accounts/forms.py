from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Order


class CreateUserForm(UserCreationForm):
    """User Creation Form"""

    class Meta:
        """CreateUserForm: Additional meta information"""

        model = User
        fields = ["username", "email", "password1", "password2"]


class OrderForm(ModelForm):
    """Order Form"""

    class Meta:
        """OrderForm: Additional meta information"""

        model = Order
        fields = "__all__"
