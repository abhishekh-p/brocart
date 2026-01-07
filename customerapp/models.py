from django.db import models
from django.contrib.auth.models import User

# models for users.

class customers(models.Model):
    LIVE = 1
    DELETE = 0
    DELETE_CHOICE = ((LIVE,'live'),(DELETE,'delete'))
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10)
    address = models.TextField()
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='customer_profile')
    delete_status = models.IntegerField(choices=DELETE_CHOICE,default=LIVE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.name