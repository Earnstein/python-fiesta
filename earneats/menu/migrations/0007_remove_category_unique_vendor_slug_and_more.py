# Generated by Django 5.0.6 on 2024-07-06 13:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("menu", "0006_alter_category_vendor"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="category",
            name="unique_vendor_slug",
        ),
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]