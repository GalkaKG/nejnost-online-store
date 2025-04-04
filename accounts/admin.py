from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'address_line1', 'address_line2', 'city', 'postal_code', 'country')
