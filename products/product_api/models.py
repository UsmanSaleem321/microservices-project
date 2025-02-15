from django.db import models

class Product(models.Model):
    user_id = models.IntegerField(null=False)  
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (user_id: {self.user_id})"

class cartitem(models.Model):
    user_id = models.IntegerField(null=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity= models.IntegerField(default=1,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return str(self.product.name)
     
    def total_price(self):
       return self.product.price * self.quantity