from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path('get_or_creat',views.get_or_create_cart,name='get_or_create'),
    path('add_to_cart/<int:pk>/',views.add_to_cart,name='add_to_cart'),
    path('view_cart_page',views.view_cart_page,name="view_cart"),
    path('checkout/',views.check_out,name='check_out'),
    path('success/', views.success_page,name='order_success'),
    path('delete/<int:id>/',views.delete_cart_item,name="delete_cart_item"),
    path("admin_order_deteail/",views.view_all_order,name="admin_order_view"),
    
]