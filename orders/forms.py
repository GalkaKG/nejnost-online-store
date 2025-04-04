from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['courier', 'delivery_type', 'delivery_address', 'office_address']

    def clean(self):
        cleaned_data = super().clean()
        delivery_type = cleaned_data.get('delivery_type')

        if delivery_type == 'home' and not cleaned_data.get('delivery_address'):
            raise forms.ValidationError('Home delivery requires an address.')
        if delivery_type == 'office' and not cleaned_data.get('office_address'):
            raise forms.ValidationError('Office delivery requires an office address.')

        return cleaned_data
