from rest_framework import serializers
from .models import Order, Order_item 
from items.models import Item # Corrected import path
from members.models import Member  # Corrected import path

class OrderItemSerializer(serializers.ModelSerializer):
    itemId = serializers.IntegerField(source='item.id')
    itemName = serializers.CharField(source='item.item_name')
    itemPrice = serializers.IntegerField(source='item.item_price')
    orderQuantity = serializers.IntegerField(source='count')
    orderStatus = serializers.CharField(source='order.status')

    class Meta:
        model = Order_item
        fields = ['itemId', 'itemName', 'itemPrice', 'orderQuantity', 'orderStatus']


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



    # def update(self, instance, validated_data):
    #     instance.member_id = validated_data.get('member_id', instance.member_id)
    #     instance.save()

    #     items_data = validated_data.pop('items')
    #     for item_data in items_data:
    #         item_id = item_data.get('itemId')
    #         if item_id:
    #             item = Order_item.objects.get(id=item_id, order=instance)
    #             item.count = item_data.get('count', item.count)
    #             item.save()
    #         else:
    #             Order_item.objects.create(order=instance, **item_data)
    #     return instance
