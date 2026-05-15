from django.db import models

# model for product

class product(models.Model):
    LIVE = 1
    DELETE = 0
    delete_choice = ((LIVE,'live'),(DELETE,'delete'))
    title = models.CharField(max_length=200)
    prize = models.FloatField()
    discription = models.TextField()
    img = models.ImageField(upload_to="image/")
    priority = models.IntegerField(default=0)
    delete_status = models.IntegerField(choices=delete_choice,default=LIVE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
