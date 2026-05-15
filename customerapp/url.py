from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path("", include('productapp.url')),
    path('register/', views.register, name='register'),
    path("login/", views.log_in, name="login"),
    
]