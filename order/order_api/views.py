from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ShippingAddress,Order
from .serilizers import ShippingAddressSerializer,OrderSerializer
from .authentication import *
from .permissions import *
from .utility import *

class ShippingAddressManagementView(APIView):
    authentication_classes = [AccountsAPIAuthentication]
    permission_classes = [IsCustomer]

    def get(self, request,pk=None):
        if pk:    
            try:
                shipping_address = ShippingAddress.objects.get(pk=pk)
                if shipping_address.user_id != request.user["id"]:
                    return Response({"error": "You do not have permission to access this shipping address."}, status=status.HTTP_403_FORBIDDEN)
                serializer = ShippingAddressSerializer(shipping_address)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ShippingAddress.DoesNotExist:
                return Response({"error": "Shipping address not found."}, status=status.HTTP_404_NOT_FOUND)
        shipping_address = ShippingAddress.objects.filter(user_id = request.user["id"])
        serializer = ShippingAddressSerializer(shipping_address, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        shipping_data=request.data
        user = request.user
        shipping_data["user_id"] = user["id"]
        serializer = ShippingAddressSerializer(data=shipping_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            shipping_address = ShippingAddress.objects.get(pk=pk)
        except ShippingAddress.DoesNotExist:
            return Response({"error": "Shipping address not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if shipping_address.user_id != request.user["id"]:
            return Response({"error": "You do not have permission to edit this shipping address."}, status=403)
        
        serializer = ShippingAddressSerializer(shipping_address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            shipping_address = ShippingAddress.objects.get(pk=pk)
        except ShippingAddress.DoesNotExist:
            return Response({"error": "Shipping address not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if shipping_address.user_id != request.user["id"]:
            return Response({"error": "You do not have permission to delete this shipping address."}, status=403)
        
        shipping_address.delete()
        return Response({"message": "Shipping address deleted successfully."}, status=status.HTTP_204_NO_CONTENT)



class getorderview(APIView):
    authentication_classes = [AccountsAPIAuthentication]

    def get(self, request):
        
        if not request.user.get('is_seller', False):
            try:
                order = Order.objects.filter(customer_id = request.user["id"])
            except order.DoesNotExist:
                return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = OrderSerializer(order, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        auth_header = request.headers.get("Authorization")     
        token = auth_header.split(" ")[1]
        Products_API_URL = "http://127.0.0.1:8001/cart/"  
        headers = {"Authorization": f"Token {token}"}
        service_token = generate_service_token()
        headers["Service-Token"] = service_token
        response = requests.get(Products_API_URL, headers=headers)
        if response.status_code != 200:
            return Response({"error": "Something went wrong."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        cart_data = response.json()
        cart_data = [item['id'] for item in cart_data if 'id' in item]
        order_data = Order.objects.filter(cart_items=cart_data )
        serializer = OrderSerializer(order_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.get('is_seller', True):
            return Response({"error": "Only customers can create orders."}, status=status.HTTP_403_FORBIDDEN)
        order_data = request.data
        order_data["customer_id"] = request.user["id"]
        serializer = OrderSerializer(data = order_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderManagementView(APIView):
    authentication_classes = [AccountsAPIAuthentication]
    permission_classes = [IsCustomer]

    
    def patch(self, request, pk):
        
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(instance=order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):

        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        order.delete()
        return Response({"message": "Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)