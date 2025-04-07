from django import forms
from .models import Order
from accounts.models import UserProfile


# forms.py

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'full_name',
            'courier',
            'delivery_type',
            'delivery_address',
            'office_address',
            'payment_method',
            'phone',
        ]

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

                if not self.initial.get('delivery_address') and profile.address_line1:
                    full_address = f"{profile.address_line1}, {profile.postal_code} {profile.city}, {profile.country}"
                    self.fields['delivery_address'].initial = full_address

            except UserProfile.DoesNotExist:
                pass
