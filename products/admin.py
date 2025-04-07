from django.contrib import admin
from .models import Color, Product, ProductVariant, Cart, CartItem
from django.utils.html import format_html


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ('color', 'price_modifier', 'image', 'image_url')
    readonly_fields = ('get_final_price',)

    def get_final_price(self, obj):
        return obj.get_final_price()

    get_final_price.short_description = 'Final Price'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'display_colors')
    search_fields = ('name', 'description')
    list_filter = ('base_price',)
    inlines = [ProductVariantInline]

    def display_colors(self, obj):
        return ", ".join([variant.color.name for variant in obj.variants.all()])

    display_colors.short_description = 'Available Colors'


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_preview')
    search_fields = ('name',)

    def color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {};"></div>',
            obj.name
        )

    color_preview.short_description = 'Preview'


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'price_modifier', 'get_final_price', 'image_preview')
    list_filter = ('product', 'color')
    search_fields = ('product__name', 'color__name')

    def get_final_price(self, obj):
        return obj.get_final_price()

    get_final_price.short_description = 'Final Price'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image.url)
        elif obj.image_url:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image_url)
        return "-"

    image_preview.short_description = 'Image Preview'


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('get_total_price',)

    def get_total_price(self, obj):
        return obj.get_total_price()

    get_total_price.short_description = 'Total Price'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'session_key', 'updated_at', 'total_price')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username',)
    inlines = [CartItemInline]
    readonly_fields = ('total_price',)

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
