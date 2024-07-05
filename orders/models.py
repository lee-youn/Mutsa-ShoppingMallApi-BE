from django.db import models
from members.models import Member
from items.models import Item

class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length = 30, default="IPRG")
    member = models.ForeignKey(Member, on_delete = models.CASCADE)
    items = models.ManyToManyField(Item,through="Order_item")

    class Meta:
        db_table = "orders"

class Order_item(models.Model):
    count = models.IntegerField()
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    class Meta:
        db_table = "order_item"