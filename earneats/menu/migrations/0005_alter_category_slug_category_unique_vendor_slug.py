# Generated by Django 5.0.6 on 2024-07-02 21:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("menu", "0004_alter_category_slug_category_unique_vendor_category"),
        ("vendor", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.CharField(max_length=100),
        ),
        migrations.AddConstraint(
            model_name="category",
            constraint=models.UniqueConstraint(
                fields=("vendor", "slug"), name="unique_vendor_slug"
            ),
        ),
    ]
