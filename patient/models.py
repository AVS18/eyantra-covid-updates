from django.db import models
from django.db.models.fields import related
from base.models import User
# Create your models here.
class Bill(models.Model):
    amount = models.IntegerField()
    description = models.CharField(max_length=2048)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=10,choices=(("Paid","Paid"),("Pending","Pending")),default="Pending")
    added_at = models.DateTimeField(auto_now_add=True)

class Report(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    description = models.CharField(max_length=200,default='')
    file = models.FileField(upload_to='reports')

class MedicalReport(models.Model):
    patient = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    spo2 = models.CharField(max_length=200)
    bp = models.CharField(max_length=200)
    sugar = models.BooleanField()
    covid = models.BooleanField()
    report = models.ManyToManyField(Report,blank=True)
