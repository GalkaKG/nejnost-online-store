from django.db import models
from django.contrib.auth.models import User

from products.models import ProductVariant


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
