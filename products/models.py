from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)  # Име на продукта
    description = models.TextField(blank=True)  # Описание (по желание)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена
    # image = models.ImageField(upload_to='products/', blank=True, null=True)  # Снимка
    image_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

