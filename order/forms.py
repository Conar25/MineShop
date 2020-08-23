from localflavor.ru.forms import RUPostalCodeField

from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    postal_code = RUPostalCodeField()
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email',
                  'city', 'address', 'postal_code')
