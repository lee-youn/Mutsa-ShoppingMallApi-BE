from rest_framework import serializers
from .models import Member, Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['city', 'street', 'zipcode']

class MemberSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False, allow_null=True)

    class Meta:
        model = Member
        fields = ['id', 'name', 'address']

    def create(self, validated_data):
        address_data = validated_data.pop('address', None)
        member = Member.objects.create(**validated_data)
        if address_data:
            Address.objects.create(member=member, **address_data)
        return member
    
    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        if address_data:
            address_instance = instance.address
            address_serializer = self.fields['address']
            address_serializer.update(address_instance, address_data)
        
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance