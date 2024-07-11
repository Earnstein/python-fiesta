# Generated by Django 5.0.6 on 2024-07-03 16:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("menu", "0005_alter_category_slug_category_unique_vendor_slug"),
        ("vendor", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="vendor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="category",
                to="vendor.vendor",
            ),
        ),
    ]