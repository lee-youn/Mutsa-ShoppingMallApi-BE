# Generated by Django 5.0.6 on 2024-07-05 18:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("items", "0003_alter_item_stock_quantity"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="item",
            name="order",
        ),
        migrations.DeleteModel(
            name="Order_item",
        ),
    ]
