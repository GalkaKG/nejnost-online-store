from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image_url')  # Добави image_url в списъка
    search_fields = ('name', 'description')


admin.site.register(Product, ProductAdmin)

