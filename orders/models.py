from django.db import models
from members.models import Member

class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length = 30, default="IPRG")
    member = models.ForeignKey(Member, on_delete = models.CASCADE)

    class Meta:
        db_table = "orders"

