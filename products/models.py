from django.db import models
from django.contrib.auth.models import User


class Color(models.Model):
    COLOR_CHOICES = [
        ('всички цветове', 'Всички цветове'),
        ('бяло', 'Бяло'),
        ('черно', 'Черно'),
        ('камел', 'Camel'),
        ('бежав', 'Nude'),
        ('розов', 'Розов'),
        ('бебешко розов', 'Бебешко розов'),
        ('син', 'Син'),
        ('сив', 'Сив'),
        ('зелен', 'Зелен'),
        ('светло син', 'Светло син'),
        ('тюркоазено', 'Тюркоазено')
    ]
    name = models.CharField(max_length=14, choices=COLOR_CHOICES, default='')
    hex_code = models.CharField(max_length=7, blank=True, null=True)

    def save(self, *args, **kwargs):
        default_hex_codes = {
            'бяло': '#ffffff',
            'черно': '#000000',
            'камел': '#c19a6b',
            'бежав': '#d9ccc2',
            'розов': '##ea558d',
            'син': '#0000ff',
            'сив': '#6f717c',
            'всички цветове': '#aaaaaa',
            'бебешко розов': '#d5aeb1',
            'светло син': '#b2d0e8',
            'тюркоазено': '#81b4b3',
            'зелен': '#11814e'
        }
        if not self.hex_code:
            self.hex_code = default_hex_codes.get(self.name, '#cccccc')
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    # Обща снимка за продукта (по желание)
    image_url = models.URLField(max_length=200, blank=True, null=True)
    main_image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    price_modifier = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # Снимка специфична за този вариант (цвят)
    image_url = models.URLField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='product_variants/', blank=True, null=True)

    def get_final_price(self):
        return self.product.base_price

    def __str__(self):
        return f"{self.product.name} - {self.color.name}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)  # Session key for anonymous users
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Cart #{self.id} - {self.user.username}"
        return f"Cart #{self.id} - Anonymous (session {self.session_key})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.variant.get_final_price() * self.quantity

    def __str__(self):
        cart_info = f"#{self.cart.id}" if self.cart else "no cart"
        return f"{self.quantity}x {self.variant} in cart {cart_info}"

