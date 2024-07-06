from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Member,Address
from .serializers import MemberSerializer

class MembersViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer = MemberSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        name = serializer.validated_data.get('name')
        address_data = serializer.validated_data.get('address')

        if address_data:
            if Address.objects.filter(
                city=address_data.get('city'),
                street=address_data.get('street'),
                zipcode=address_data.get('zipcode')
            ).exists():
                return Response({'detail': '동일한 주소를 가진 멤버가 이미 존재합니다.'}, status=status.HTTP_409_CONFLICT)

        member = serializer.save()
        member_serializer = MemberSerializer(member)
        return Response(member_serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        queryset = Member.objects.all()
        serializer = MemberSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        try:
            member = Member.objects.get(pk=pk)
        except Member.DoesNotExist:
            return Response({'detail': '해당 멤버를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MemberSerializer(member)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def partial_update(self, request, pk=None):
        try:
            member = Member.objects.get(pk=pk)
        except Member.DoesNotExist:
            return Response({'detail': '해당 멤버를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MemberSerializer(member, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        member = serializer.save()
        member_serializer = MemberSerializer(member)
        return Response(member_serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk=None):
        try:
            member = Member.objects.get(pk=pk)
        except Member.DoesNotExist:
            return Response({'detail': '해당 멤버를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
