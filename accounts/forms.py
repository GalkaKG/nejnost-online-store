from django import forms
from django.contrib.auth.models import User

from .models import UserProfile


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(label="Потребител")
    email = forms.EmailField(label="Имейл")
    password = forms.CharField(widget=forms.PasswordInput, label="Парола")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Потвърди паролата")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Паролите не съвпадат.")


class UserProfileForm(forms.ModelForm):
    full_name = forms.CharField(label="Име и Презиме")
    phone_number = forms.CharField(label="Телефонен номер")
    address_line1 = forms.CharField(label="Адрес")
    city = forms.CharField(label="Град")
    postal_code = forms.CharField(label="Пощенски код")
    country = forms.CharField(label="Държава")

    class Meta:
        model = UserProfile
        fields = ['full_name', 'phone_number', 'address_line1', 'city', 'postal_code', 'country']
