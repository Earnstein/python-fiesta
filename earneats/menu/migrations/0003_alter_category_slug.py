# Generated by Django 5.0.6 on 2024-07-02 19:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("menu", "0002_alter_category_category_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.CharField(max_length=100),
        ),
    ]
