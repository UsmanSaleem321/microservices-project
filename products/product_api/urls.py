from django.urls import path
from .views import *

urlpatterns = [
    path("product/", ProductManagementView.as_view()),
    path("product/<int:pk>/",ProductManagementView.as_view()),
    path("cart/",Cart_Get_view.as_view()),
    path("cart/<int:pk>/",Cart_Management_View.as_view()),
]