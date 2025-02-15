import requests
from .models import Product
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from.authentication import AccountsAPIAuthentication, CartServiceAuthentication
from.permissions import *
from django.shortcuts import get_object_or_404
from .models import Product, cartitem    
from .utility import validate_servicet_token
class ProductManagementView(APIView):
    authentication_classes = [AccountsAPIAuthentication]
    permission_classes = [IsSeller]
    
    def get_permissions(self):
       
        if self.request.method == 'GET':
            return []
        return [IsSeller()]  

    def get(self, request, pk=None):
        user = request.user
        if pk:    
            try:
                product = Product.objects.get(id=pk)
            except Product.DoesNotExist:
                return Response({"error": "Product not found."}, status=404)
            serializer = ProductSerializer(product)
            return Response(serializer.data)    
        
        if user.get("is_seller", False):
            products = Product.objects.filter(user_id=user["id"])
        else:
            products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def post(self, request):
        
        user = request.user  
        if not user.get("is_seller", False): 
           return Response({"error": "Only sellers can create products."}, status=403)
        product_data = request.data
        product_data ["user_id"] = user["id"]
        serializer = ProductSerializer(data=product_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product created successfully!"})
        return Response(serializer.errors, status=400) 
        

    def patch(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=404)

        if product.user_id != request.user["id"]:
            return Response({"error": "You do not have permission to edit this product."}, status=403)

        serializer = ProductSerializer(instance=product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product edited successfully!", "product": serializer.data}, status=200)
        return Response(serializer.errors, status=400)

    
    def delete(self,request,pk):
        try:
          product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=404)
        if product.user_id != request.user["id"]:
            return Response({"error": "You do not have permission to delete this product."}, status=403)
        product.delete()
        return Response({"message": "Product deleted successfully!"})

class Cart_Get_view(APIView):
    authentication_classes = [AccountsAPIAuthentication]

    def get(self,request):
        if request.user.get("is_seller", True):
            service_token = request.headers.get("service-token")
            if not service_token:
                return Response({"error": "Service token is required."}, status=status.HTTP_403_FORBIDDEN)
            check = validate_servicet_token(service_token)
            if check:
                products = Product.objects.filter(user_id=request.user["id"])
                cart = cartitem.objects.filter(product__in=products)
                serializer = CartItemSerializer(cart, many=True)
                return Response(serializer.data)    
                 
        else:    
            cart = cartitem.objects.filter(user_id=request.user["id"])
            serializer = CartItemSerializer(cart, many=True)
            return Response(serializer.data)                                                                                                

    def post(self,request):       
        user = request.user 
        if user.get("is_seller", True):
            return Response({"error": "Only customers can add items to the cart."}, status=status.HTTP_403_FORBIDDEN)    
        cart_item_data = request.data
        cart_item_data['user_id'] = request.user["id"]
        serializer = CartItemSerializer(data=cart_item_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Cart item created successfully!", "cart_item": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
       
class Cart_Management_View(APIView):
    authentication_classes = [AccountsAPIAuthentication]
    permission_classes = [IsCustomer]
    
    def get(self,request,pk):
        try:
            cart = cartitem.objects.get(id=pk)
        except cartitem.DoesNotExist:
            return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CartItemSerializer(cart)
        return Response(serializer.data)   
    
    def patch(self, request, pk):
        try:
            item = cartitem.objects.get(id=pk)
        except item.DoesNotExist:
            return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if item.user_id != request.user["id"]:
            return Response({"error": "You do not have permission to edit this cart item."}, status=status.HTTP_403_FORBIDDEN)

        serializer = CartItemSerializer(instance=item, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Cart item updated successfully!", "cart_item": serializer.data})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            cart_item = cartitem.objects.get(id=pk)
        except cartitem.DoesNotExist:
            return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

        if cart_item.user_id != request.user["id"]:
            return Response({"error": "You do not have permission to delete this cart item."}, status=status.HTTP_403_FORBIDDEN)

        cart_item.delete()

        return Response({"message": "Cart item deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

