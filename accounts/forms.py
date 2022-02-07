from django.forms import ModelForm

from .models import Order


class OrderForm(ModelForm):
    """Order Form"""

    class Meta:
        """OrderForm: Additional meta information"""

        model = Order
        fields = "__all__"
