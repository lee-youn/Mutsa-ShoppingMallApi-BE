from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Item
from .serializers import ItemsSerializer

class ItemsViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = ItemsSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        item = serializer.save()
        item_serializer = ItemsSerializer(item)
        return Response(item_serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        queryset = Item.objects.all()
        serializer = ItemsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        try:
            item = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return Response({'detail': '해당 아이템을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ItemsSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def partial_update(self, request, pk=None):
        try:
            item = Item.objects.get(pk=pk)
        except item.DoesNotExist:
            return Response({'detail': '해당 아이템을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ItemsSerializer(item, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        item = serializer.save()
        item_serializer = ItemsSerializer(item)
        return Response(item_serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk=None):
        try:
            item = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return Response({'detail': '해당 아이템을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
