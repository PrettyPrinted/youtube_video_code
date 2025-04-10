from rest_framework import serializers 
from .models import Product, Coupon

class CouponSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField(max_length=10)
    discount = serializers.IntegerField()
    active = serializers.BooleanField()

    def create(self, validated_data):
        return Coupon.objects.create(**validated_data)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'