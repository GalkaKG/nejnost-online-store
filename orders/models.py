from django.conf import settings
from django.db import models


class Order(models.Model):
    COURIER_CHOICES = [
        ('Speedy', 'Speedy'),
        ('Econt', 'Econt'),
    ]

    PAYMENT_CHOICES = [
        ('cod', 'Наложен платеж'),
        ('bank', 'Банков превод'),
        ('card', 'Карта (Stripe)'),
    ]

    DELIVERY_CHOICES = [
        ('home', 'До адрес'),
        ('office', 'До офис на куриер'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True)
    courier = models.CharField(max_length=20, choices=COURIER_CHOICES)
    delivery_type = models.CharField(max_length=10, choices=DELIVERY_CHOICES)

    delivery_address = models.CharField("Адрес за доставка", max_length=255, blank=True, null=True)
    office_address = models.CharField("Офис на куриер", max_length=255, blank=True, null=True)

    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)

    phone = models.CharField(max_length=20, blank=True, null=True)

    city = models.CharField(max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=50, default='в процес')


    def save(self, *args, **kwargs):
        if self.delivery_type == 'home':
            self.office_address = None
        elif self.delivery_type == 'office':
            self.delivery_address = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Поръчка #{self.id} от {self.user.username}"


