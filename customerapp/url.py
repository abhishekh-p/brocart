from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path("", include('productapp.url')),
    path("ordersapp",include('ordersapp.url')),
    path('register/', views.register, name='register'),
    path("login/", views.log_in, name="login"),
    path('logout/',views.log_out,name="logout"),
    path('customer_profile/',views.customer_profile,name="customer_profile"),
    path('products_details/<int:pk>/', views.product_detail,name='product_details'),
    path('update_profile',views.update_profile,name='update_profile'),

    
]