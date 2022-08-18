from django import forms

from .models import Order

class OrderForm(forms.ModelForm):
    """ Order form """
    class Meta:
        """ Order form """
        model = Order
        fields = (
            'full_name',
            'email',
            'phone_number',
        )