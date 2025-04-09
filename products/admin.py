from django.contrib import admin
from .models import Color, Product, ProductVariant
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

