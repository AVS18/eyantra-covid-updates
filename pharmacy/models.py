from random import choice
from django.db import models
from django.db.models.fields import related
from base.models import User
from patient.models import Bill
# Create your models here.
class Medicine(models.Model):
    name = models.CharField(max_length=2048)
    image = models.ImageField(upload_to='medicines')
    description = models.CharField(max_length=2048)
    cost = models.IntegerField()
    expiry_date = models.DateField()
    expected_delivery = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class Order(models.Model):
    medicine = models.ForeignKey(Medicine,on_delete=models.SET_NULL,null=True)
    ordered_by = models.ForeignKey(User,related_name='ordered_by',on_delete=models.DO_NOTHING)
    ordered_to = models.ForeignKey(User,related_name='ordered_to',on_delete=models.DO_NOTHING)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15,choices=(('Cancelled','Cancelled'),('Pending','Pending'),('Accepted','Accepted'),('Rejected','Rejected'),('Shipped','Shipped')))
    tracking_id = models.CharField(max_length=500,blank=True,null=True)
    service = models.CharField(max_length=250,blank=True,null=True)
    receipt = models.ImageField(upload_to='orders',blank=True,null=True)
    billing = models.ForeignKey(Bill,on_delete=models.SET_NULL,null=True)
