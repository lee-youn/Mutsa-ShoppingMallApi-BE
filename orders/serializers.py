from rest_framework import serializers
from .models import Order, Order_item, OrderStatus
from items.models import Item # Corrected import path
from members.models import Member  # Corrected import path

class OrderItemSerializer(serializers.ModelSerializer):
    itemId = serializers.IntegerField(source='item.id')
    itemName = serializers.CharField(source='item.item_name')
    itemPrice = serializers.IntegerField(source='item.item_price')
    orderQuantity = serializers.IntegerField(source='count')

    class Meta:
        model = Order_item
        fields = ['itemId', 'itemName', 'itemPrice', 'orderQuantity']



class OrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    items = OrderItemSerializer(source='order_item_set', many=True)

    class Meta:
        model = Order
        fields = ['id', 'member','order_date','items','status']
        


class OrderItemRequestDTO(serializers.Serializer):
    itemId = serializers.IntegerField()
    orderQuantity = serializers.IntegerField()


class OrderRequestDTO(serializers.Serializer):
    memberId = serializers.IntegerField()
    items = serializers.ListField(
        child=serializers.DictField()
    )

class MemberOrderItemSerializer(serializers.ModelSerializer):
    member_id = serializers.IntegerField()
    orders = OrderSerializer(source='order_item_set', many=True, read_only=True)

    class Meta:
        model = Member
        fields = ['memberId', 'orders']


class CancelOrderItemSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=OrderStatus.choices)
