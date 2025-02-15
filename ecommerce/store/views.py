from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseForbidden

class SellerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'seller':
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("You do not have permission to access this page.")
    
class loginview(View):
    
    def get(self,request,*args, **kwargs):
        form = AuthenticationForm()
        context = {
            "form":form
        }
        return render(request,"store/login.html", context)
    
    def post(self,request,*args, **kwargs):
        form  = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect("store")

class signupview(View):
    def get(self,request,*args, **kwargs):
        form = CustomUserCreationForm()
        context = {
            "form":form
            }
        return render(request,"store/signup.html",context)
    def post(self,request,*args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfulu.')
            return redirect("login")

class logoutview(LoginRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        if request.user.role == "seller":
            returning = "seller"
        else:
            returning = "customer"
        logout(request)
        if returning == "seller":
            return redirect("seller_login")
        else:
            return redirect("store")

class storeview(View):
    def get(self,request,*args, **kwargs):
        products = Product.objects.all()
        user = request.user
        if user.is_authenticated:
           if user.role == "seller":
               return redirect("seller_home")
           customer = Customer.objects.get(id=self.request.user.id)
           cart_item = cartitem.objects.filter(customer = customer)    
           cart_item_count = cart_item.count()
           context = {
            "products":products,
            "cart_item_count":cart_item_count
                 }
           return render(request, "store/store.html", context )
        context = {
            "products":products
                 }
        return render(request, "store/store.html", context )

class addtocartview(LoginRequiredMixin,View):
    def get(self,request,pk,*args, **kwargs):
        product = Product.objects.get(id=pk)
        user=request.user
        customer = Customer.objects.get(user=user)
        cart_item, created = cartitem.objects.get_or_create(
        product=product,
        customer=customer,
            )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
            return redirect("store")
        return redirect("store")
    
    def post(self,request,pk,*args, **kwargs):
        cart_item = cartitem.objects.get(id=pk)
        action = request.POST.get("action")
        if (cart_item.quantity == 0)&(action != "increase"):
            return redirect("cart")
        elif(action == "increase"):
            cart_item.quantity +=1
        elif(action == "delete"):
            cart_item.delete()
            return redirect("cart")
        else:
            cart_item.quantity -=1
        cart_item.save()
        return redirect("cart") 
            
class cartview(LoginRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        cart_items = customer.cart_items.all()
        total_price = sum(item.product.price * item.quantity for item in customer.cart_items.all())
        cart_item_count = cart_items.count()
        context = {
           "cart_items":cart_items,
           "cart_item_count":cart_item_count,
           "total_price":total_price
        }
        return render(request, "store/cart.html", context )
    
class orderview(LoginRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        
        customer = Customer.objects.get(user=request.user)
        cart_items = cartitem.objects.filter(customer = customer)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        if not created:
            order.cart_items.clear()  
            order.cart_items.add(*cart_items)  
        else:
            order.cart_items.add(*cart_items)
        total_price = sum(item.product.price * item.quantity for item in customer.cart_items.all())
        cart_item_count = cart_items.count
        context = {
            'order': order,
            'cart_items': cart_items,
            "total_price":total_price,
            "cart_item_count":cart_item_count,
        }
        return render(request, "store/ordersummary.html", context)
    
    def post(self,request,*args, **kwargs):
        form = ShippingAddressForm(request.POST)
        if form.is_valid:
            shipping_detail = form.save()    
        customer = Customer.objects.get(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        if not created:
            order.shipping_detail = shipping_detail
            order.transaction_id = '123456'
            order.complete = True
            order.save()
            messages.success(request,"order completed successfuly")
        return redirect("store")

class producte_editview(SellerRequiredMixin,UserPassesTestMixin,LoginRequiredMixin,View):

    
    def get(self,request,pk,*args, **kwargs):
        product = Product.objects.get(id=pk)
        form = ProdcutForm(instance=product)
        context = {
            "form":form,
            "product":product
        }
        return render(request, "store/edit_product.html",context)
    
    def post(self,request,pk,*args, **kwargs):
        product = Product.objects.get(id=pk)
        form = ProdcutForm(request.POST,request.FILES,instance=product)
        if form.is_valid:
            form.save()
            return redirect("seller_home")

    def test_func(self):
        pk = self.kwargs.get('pk')
        product = Product.objects.get(id=pk) 
        print(self.request.user)
        print(product.seller)
        return self.request.user == product.seller.user

class seller_login_view(View):
    
    def get(self,request,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect("seller_home")
        form = AuthenticationForm()
        context = {
            "form":form
        }
        return render(request,"store/login_seller.html", context)
    
    def post(self,request,*args, **kwargs):
        form  = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect("seller_home")

class seller_signup_view(View):
    def get(self,request,*args, **kwargs):
        form = CustomUserCreationForm()
        context = {
            "form":form,
            "role":"seller"
        }
        return render(request,"store/signup.html",context)
    
    def post(self,request,*args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "seller"
            user.save()
            messages.success(request, 'User created successfully.')
            return redirect("seller_login")

class seller_home_view(SellerRequiredMixin,LoginRequiredMixin,View):
    def get(self, request,*args, **kwargs):
        products = Product.objects.filter(seller=request.user.seller)
        context = {
            "products":products
        }
        return render(request,"store/seller_home.html",context)

class addproduct_view(SellerRequiredMixin,LoginRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        form = ProdcutForm()
        context = {
         "form":form
        }
        return render(request,"store/add_product.html", context )
    def post(self,request,*args, **kwargs):
        form = ProdcutForm(data=request.POST, files=request.FILES)
        if form.is_valid:
            product = form.save(commit=False)
            product.seller = self.request.user.seller
            product.save()
            return redirect("seller_home")

class delete_product_view(UserPassesTestMixin,SellerRequiredMixin,LoginRequiredMixin,View):
    
    def get(self,request,pk,*args, **kwargs):
        product = Product.objects.get(id=pk)
        if request.user.seller == product.seller:
            product.delete()
            return redirect("seller_home")
        return redirect("store")
    
    def test_func(self):
        pk = self.kwargs.get('pk')
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return False  
        if self.request.user == product.seller.user:
            return True

class seller_order_view(SellerRequiredMixin,LoginRequiredMixin,View):
    
    def get(self,request,*args, **kwargs):
        seller = request.user.seller
        orders = Order.objects.filter(
            cart_items__product__seller=seller
        ).distinct()

        context = {
            "orders": orders
              }
        return render(request, "store/seller_orders.html", context)