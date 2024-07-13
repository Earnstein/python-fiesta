# Generated by Django 5.0.6 on 2024-07-12 21:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("marketplace", "0003_alter_cart_quantity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="quantity",
            field=models.PositiveIntegerField(default=1, verbose_name="Quantity"),
        ),
    ]
