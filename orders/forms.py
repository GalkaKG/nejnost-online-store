from django import forms

from accounts.models import UserProfile
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'full_name',
            'phone',
            'city',
            'courier',
            'delivery_type',
            'delivery_address',
            'office_address',
            'payment_method',
        ]

    # full_name = forms.CharField(label="Име и Презиме")
    # phone = forms.CharField(label="Телефонен номер")
    # city = forms.CharField(label="Град")
    # delivery_address = forms.CharField(label="Адрес")
    # courier = forms.CharField(label="Куриер")
    # delivery_type = forms.CharField(label="Избери вид на доставката")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            try:
                profile = user.userprofile

                if not self.initial.get('full_name'):
                    self.fields['full_name'].initial = profile.full_name

                if not self.initial.get('phone'):
                    self.fields['phone'].initial = profile.phone_number

                if not self.initial.get('city'):
                    self.fields['city'].initial = profile.city

                if not self.initial.get('delivery_address') and profile.address_line1:
                    full_address = f"{profile.address_line1}, {profile.postal_code} {profile.city}, {profile.country}"
                    self.fields['delivery_address'].initial = full_address

            except UserProfile.DoesNotExist:
                pass
