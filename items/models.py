from django.db import models
from orders.models import Order

class Item(models.Model):
    item_name = models.CharField(max_length=30)
    stock_quantity = models.IntegerField()
    item_price = models.IntegerField()
    order = models.ManyToManyField(Order,through="Order_item")

    class Meta:
        db_table = "item"

class Order_item(models.Model):
    count = models.IntegerField()
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    class Meta:
        db_table = "order_item"