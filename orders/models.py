from django.db import models
from django.conf import settings


class Order(models.Model):
    COURIER_CHOICES = [
        ('Speedy', 'Speedy'),
        ('Econt', 'Econt'),
    ]

    DELIVERY_CHOICES = [
        ('home', 'Home Address'),
        ('office', 'Office'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    courier = models.CharField(max_length=20, choices=COURIER_CHOICES)
    delivery_type = models.CharField(max_length=10, choices=DELIVERY_CHOICES)
    delivery_address = models.CharField(max_length=255, null=True, blank=True)
    office_address = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

