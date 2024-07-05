from django.db import models

class Item(models.Model):
    item_name = models.CharField(max_length=30)
    stock_quantity = models.IntegerField()
    item_price = models.IntegerField()

    class Meta:
        db_table = "item"