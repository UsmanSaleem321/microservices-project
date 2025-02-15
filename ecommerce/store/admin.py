from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Seller)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(cartitem)
admin.site.register(ShippingAddress)

