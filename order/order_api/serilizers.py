from rest_framework import serializers
from .models import ShippingAddress, Order

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['id','user_id', 'address', 'city', 'state', 'country', 'zipcode']
        read_only_fields = ['id']
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer_id', 'cart_items', 'date_ordered', 'complete', 'shipping_detail']
        read_only_fields = ['id', 'date_ordered'] 

    
