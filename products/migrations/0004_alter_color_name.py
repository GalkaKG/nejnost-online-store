# Generated by Django 5.1.7 on 2025-04-06 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0003_alter_color_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="color",
            name="name",
            field=models.CharField(
                choices=[
                    ("всички цветове", "Всички цветове"),
                    ("бяло", "Бяло"),
                    ("черно", "Черно"),
                    ("камел", "Camel"),
                    ("бежав", "Nude"),
                    ("розов", "Розов"),
                    ("бебешко розов", "Бебещко розов"),
                    ("син", "Син"),
                    ("сив", "Сив"),
                    ("зелен", "Зелен"),
                    ("светло син", "Светло син"),
                    ("тюркоазено", "Тюркоазено"),
                ],
                default="",
                max_length=14,
            ),
        ),
    ]
