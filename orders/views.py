from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Order, Order_item, OrderStatus
from .serializers import OrderSerializer,OrderRequestDTO,MemberOrderItemSerializer,CancelOrderItemSerializer
from members.models import Member
from items.models import Item


class OrdersViewSet(viewsets.ViewSet):
    def create(self, request):
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

            # # Check if order quantity is available in stock
            if item.stock_quantity < order_item_data['orderQuantity']:
                raise ValidationError(f"상품 {item.item_name}의 재고가 부족합니다.")
            
            # # Update stock quantity
            item.stock_quantity -= order_item_data['orderQuantity']
            item.save()  # 변경된 재고 수량 저장

            order_items.append(Order_item(
                order=order,
                item=item,
                count=order_item_data['orderQuantity']
            ))

        order.save()  # 주문 저장
        for order_item in order_items:
            order_item.save()  # 주문 항목 저장
        for item in items:
            item.save()  # 상품 저장    order.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def list(self, request):
        member_id = request.query_params.get('member_id')

        if not member_id:
            return Response({'detail': 'Member ID must be provided in query parameters.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            queryset = Order.objects.filter(member = member_id)
        except ValueError:
            return Response({'detail': 'Invalid member ID format.'}, status=status.HTTP_400_BAD_REQUEST)

        member = Member.objects.get(id=int(member_id))
        serializer = OrderSerializer(queryset, many=True)

        response_data = {
            'member_id': member.id,
            'orders': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    
    def retrieve(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'detail': '해당 주문을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def partial_update(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'detail': '해당 주문을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderSerializer(order, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        order = serializer.save()
        order_serializer = OrderSerializer(order)
        return Response(order_serializer.data, status=status.HTTP_200_OK)
    
    
    def destroy(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'detail': '해당 주문을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


    @action(detail=True, methods=['get'])
    def cancel(self, request, pk=None):
        try:
            order = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return Response({'detail': '해당 주문을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        if order.status == OrderStatus.CANCEL:
            return Response({'detail': '주문이 이미 취소 상태입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = OrderStatus.CANCEL
        order.save()  # 상태 업데이트 후 저장

        data = Order.objects.get(id=pk)
        data_serializer = OrderSerializer(data)
        return Response(data_serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def done(self, request, pk=None):
        try:
            order = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return Response({'detail': '해당 주문을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        if order.status == OrderStatus.DONE:
            return Response({'detail': '주문이 이미 완료 상태입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = OrderStatus.DONE
        order.save()  # 상태 업데이트 후 저장

        data = Order.objects.get(id=pk)

        data_serializer = OrderSerializer(data)
        return Response(data_serializer.data, status=status.HTTP_200_OK)