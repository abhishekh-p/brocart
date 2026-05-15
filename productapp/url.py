from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path('', views.index),
    path('products/', views.list_product,name='home'),
    path('products_details/<int:pk>/', views.product_detail,name='product_details'),
    
]