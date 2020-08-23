from localflavor.ru.forms import RUPostalCodeField

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Order


class OrderForm(forms.ModelForm):
    postal_code = RUPostalCodeField(label=_('Postal Code'))
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email',
                  'city', 'address', 'postal_code')
