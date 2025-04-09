from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('get_total_price',)

    def get_total_price(self, obj):
        return obj.get_total_price()

    get_total_price.short_description = 'Total Price'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user_display', 'created_at', 'session_key', 'updated_at', 'total_price')
    list_filter = ('created_at', 'updated_at', 'user')
    search_fields = ('user__username', 'session_key',)
    inlines = [CartItemInline]
    readonly_fields = ('total_price',)

    def user_display(self, obj):
        return obj.user.username if obj.user else "Anonymous"

    user_display.short_description = 'User'

    def total_price(self, obj):
        return sum(item.get_total_price() for item in obj.items.all())

    total_price.short_description = 'Total Cart Value'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'variant', 'quantity', 'get_total_price')
    list_filter = ('cart__user',)
    search_fields = ('variant__product__name', 'variant__color__name')

    def get_total_price(self, obj):
        return obj.get_total_price()

    get_total_price.short_description = 'Total Price'

