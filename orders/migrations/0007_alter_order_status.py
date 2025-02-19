# Generated by Django 5.0.6 on 2024-07-06 17:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0006_alter_order_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.TextField(
                choices=[
                    ("IPRG", "In progress"),
                    ("DONE", "Done"),
                    ("CANCLE", "Cancle"),
                ],
                default="IPRG",
                max_length=128,
            ),
        ),
    ]
