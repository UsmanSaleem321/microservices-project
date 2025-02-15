from django.urls import path
from .views import *

urlpatterns = [
   
    path('shipping-address/', ShippingAddressManagementView.as_view(), name='shipping_address_list_create'),
    path('shipping-address/<int:pk>/', ShippingAddressManagementView.as_view(), name='shipping_address_detail'),
    path('order/', getorderview.as_view()),
    path('order/<int:pk>/', OrderManagementView.as_view()),
    
]