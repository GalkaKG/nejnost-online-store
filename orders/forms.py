from django import forms

from accounts.models import UserProfile
from .models import Order


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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            # Ако потребителят е логнат, използвай данни от неговия профил
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
        else:
            # Ако потребителят не е логнат, прави полетата задължителни
            self.fields['full_name'].required = True
            self.fields['phone'].required = True
            self.fields['city'].required = True
            self.fields['delivery_address'].required = True
