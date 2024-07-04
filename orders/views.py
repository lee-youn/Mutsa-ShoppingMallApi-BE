from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer,OrderRequestDTO
from members.models import Member
from items.models import Item, Order_item

class OrdersViewSet(viewsets.ViewSet):
    def create(self, request):
        print(request.data)
        serializer = OrderRequestDTO(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data

        try:
            member = Member.objects.get(id=data.get('memberId'))
        except Member.DoesNotExist:
            raise ValidationError('해당 memberId를 가진 사용자가 존재하지 않습니다.')

        if 'items' not in data or not data['items']:
            raise ValidationError('주문할 상품을 선택해야 합니다.')

        order = Order(member=member)
        order_items = []
        items = []

        for order_item_data in data['items']:
            try:
                item = Item.objects.get(id=order_item_data.get('itemId'))
            except Item.DoesNotExist:
                raise ValidationError(f"해당 itemId ({order_item_data.get('itemId')})를 가진 상품이 존재하지 않습니다.")

            if 'orderQuantity' not in order_item_data:
                raise ValidationError('주문 수량이 필요합니다.')

            # Check if order quantity is available in stock
            if item.stock_quantity < order_item_data['orderQuantity']:
                raise ValidationError(f"상품 {item.item_name}의 재고가 부족합니다.")

            item.stock_quantity(order_item_data['orderQuantity'], save=False)
            items.append(item)
            order_items.append(Order_item(
                order=order,
                item=item,
                count=order_item_data['orderQuantity']
            ))
        
        order.save()
        for order_item in order_items:
            order_item.save()
        for item in items:
            item.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def list(self, request):
        member_id = request.query_params.get('memberId')
        queryset = Order.objects.filter(member_id=member_id)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'detail': '해당 주문을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'detail': '해당 주문을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# from rest_framework import viewsets
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Order
# from .serializers import OrderSerializer

# class OrdersViewSet(viewsets.ViewSet):
#     def create(self, request):
#         serializer = OrderSerializer(data=request.data)

#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         order = serializer.save()
#         order_serializer = OrderSerializer(order)
#         return Response(order_serializer.data, status=status.HTTP_201_CREATED)
    
#     def list(self, request):
#         member_id = request.query_params.get('memberId')
#         queryset = Order.objects.filter(member_id=member_id)
#         serializer = OrderSerializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def retrieve(self, request, pk=None):
#         try:
#             order = Order.objects.get(pk=pk)
#         except Order.DoesNotExist:
#             return Response({'detail': '해당 주문을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
#         serializer = OrderSerializer(order)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def destroy(self, request, pk=None):
#         try:
#             order = Order.objects.get(pk=pk)
#         except Order.DoesNotExist:
#             return Response({'detail': '해당 주문을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
#         order.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)