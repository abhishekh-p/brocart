from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    
    path('', views.index),
    # path('admin_dasboard/',include('customerapp.url')),
    path('products/', views.list_product,name='home'),
    path('products_details/<int:pk>/', views.product_detail,name='product_details'),
    path('admin_home/',views.admin_home_page,name="admin_home"),
    path('add_product/',views.add_prduct,name="add_product"),
    path('search_product',views.search_list_product,name="search_product"),
    path('delete_product/<int:pk>',views.delete_product,name="delete_product"),
    path('edit_product/<int:pk>',views.edit_product,name="edit_product"),
    path('admin_search_product',views.admin_search_product,name="admin_search_product"),
]
if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
