from django.contrib import admin
from django.urls import path, include
from store.views import *

urlpatterns = [

    path("", storeview.as_view(), name = "store"),
    path("login/", loginview.as_view(), name="login"),
    path("logout/", logoutview.as_view(), name="logout"),
    path("signup/",signupview.as_view(), name = "signup"),
    path("cart/", cartview.as_view(), name= "cart"),
    path("addcart/<int:pk>",addtocartview.as_view(), name="addcart"),
    path("checkout/",orderview.as_view(), name= "order"),
    path("seller/product/<int:pk>/",producte_editview.as_view(), name="edit_product"),
    path("seller_signup/", seller_signup_view.as_view(), name="seller_signup"),
    path("seller/login/", seller_login_view.as_view(), name = "seller_login"),
    path("seller/home/", seller_home_view.as_view(), name="seller_home" ),
    path("seller/add_product/", addproduct_view.as_view(), name= "add_product"),
    path("seller/delete_product/<int:pk>/", delete_product_view.as_view(), name= "delete_product"),
    path("seller/orders/",seller_order_view.as_view(), name="seller_order"),
    
]
