from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'full_name', 'user', 'courier', 'delivery_type',
        'get_delivery_address', 'city', 'payment_method', 'status', 'created_at'
    )
    list_filter = ('courier', 'delivery_type', 'payment_method', 'city', 'status', 'created_at')
    search_fields = ('full_name', 'user__username', 'phone')
    ordering = ('-created_at',)

    def get_delivery_address(self, obj):
        if obj.delivery_type == 'office':
            return obj.office_address or "—"
        elif obj.delivery_type == 'home':
            return obj.delivery_address or "—"
        return "—"

    get_delivery_address.short_description = 'Адрес на доставка'


