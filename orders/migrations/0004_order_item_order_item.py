# Generated by Django 5.0.6 on 2024-07-05 18:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("items", "0004_remove_item_order_delete_order_item"),
        ("orders", "0003_alter_order_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order_item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("count", models.IntegerField()),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="items.item"
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="orders.order"
                    ),
                ),
            ],
            options={
                "db_table": "order_item",
            },
        ),
        migrations.AddField(
            model_name="order",
            name="item",
            field=models.ManyToManyField(through="orders.Order_item", to="items.item"),
        ),
    ]
