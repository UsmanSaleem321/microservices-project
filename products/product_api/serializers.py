from rest_framework import serializers
from .models import Product, cartitem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'created_at', 'updated_at', 'user_id']
        read_only_fields = ['id', 'created_at', 'updated_at']

class CartItemSerializer(serializers.ModelSerializer):
   
    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    
    class Meta:
        model = cartitem
        fields = ['id', 'user_id', 'product', 'quantity', 'date_added', 'total_price']
        read_only_fields = ['id', 'date_added', 'total_price']