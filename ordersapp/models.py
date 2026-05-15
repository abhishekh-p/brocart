from django.db import models
from customerapp.models import customers
from productapp.models import product

# models for cart
class order(models.Model):
    LIVE = 1
    DELETE = 0
    DELETE_CHOICE = ((LIVE,'live'),(DELETE,'delete'))
    cart_stage = 0
    ORDER_CONFIRMED = 1
    ORDER_PROCESSED = 2
    ORDER_DELIVERD = 3
    ORDER_DELETED = 4
    STATUS_CHOISE = ((cart_stage,"cart"),
                     (ORDER_CONFIRMED,"ORDER CONFIRMED"),
                     (ORDER_PROCESSED,"ORDER_PROCESSED"),
                     
                     (ORDER_DELIVERD,"ORDER_DELIVERD"),
                     (ORDER_DELETED,"ORDER_DELETED")
                     )
    ORDER_STATUS = models.IntegerField(choices=STATUS_CHOISE,default=cart_stage)
    owner = models.ForeignKey(customers,on_delete=models.SET_NULL,null=True,related_name='order')
    delete_status = models.IntegerField(choices=DELETE_CHOICE,default=LIVE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class  orderItem(models.Model):
    order = models.ForeignKey(order,on_delete=models.CASCADE,related_name='order_item')
    products = models.ForeignKey(product,on_delete=models.SET_NULL,null=True,related_name="added_cart")
    quantity = models.IntegerField(default=1)

class payment(models.Model):
    payment_cod = 1
    payment_online = 2
    payment_choice = (
                (payment_cod,'cash on delivery'),
                (payment_online,'payment online')
                      )
    
    payment_method = models.IntegerField(choices=payment_choice,default=payment_cod)
    
    payment_order =models.ForeignKey(order,on_delete=models.CASCADE,related_name='order_payment')
    creates_date = models.DateTimeField(auto_now_add=True)