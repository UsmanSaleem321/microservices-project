from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_ROLES = (
        ('customer', 'Customer'),
        ('seller', 'Seller'),
    )
    role = models.CharField(max_length=10, choices=USER_ROLES, default='customer')


class Seller(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE) 

    def __str__(self):
        return self.user.username
class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length = 200, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='images/', default='images/placeholder.png')

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True, null=True)
    def __str__(self):
        return self.user.username


class cartitem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="cart_items", null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity= models.IntegerField(default=1,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return str(self.product.name)
     
    def total_price(self):
       return self.product.price * self.quantity

class ShippingAddress(models.Model):
    address = models.CharField(max_length = 200, null=True)
    city = models.CharField(max_length = 200, null=True)
    state = models.CharField(max_length = 200, null=True)
    country = models.CharField(max_length = 200, null=True)
    zipcode = models.CharField(max_length = 200, null=True)
    def __str__(self):
        return self.address



class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    cart_items = models.ManyToManyField(cartitem, blank=True) 
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id= models.CharField(max_length=100, null=True)
    shipping_detail = models.OneToOneField(ShippingAddress, on_delete=models.CASCADE, null=True, blank=True) 
    def __str__(self):
        return str(self.id)
 



@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        if instance.role == "customer":
            Customer.objects.create(user=instance)
        elif instance.role == "seller":
            Seller.objects.create(user=instance)

