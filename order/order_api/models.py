from django.db import models


class ShippingAddress(models.Model):
    user_id = models.IntegerField()
    address = models.CharField(max_length = 200, null=True)
    city = models.CharField(max_length = 200, null=True)
    state = models.CharField(max_length = 200, null=True)
    country = models.CharField(max_length = 200, null=True)
    zipcode = models.CharField(max_length = 200, null=True)
    def __str__(self):
        return self.address


class Order(models.Model):
    customer_id = models.IntegerField()  
    cart_items = models.JSONField("Cart Item IDs", default=list)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    shipping_detail = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True) 
    
    def __str__(self):
        return f"Order {self.id}"