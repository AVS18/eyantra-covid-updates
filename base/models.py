from django.db import models
from django.contrib.auth.models import AbstractUser
from django_clamd.validators import validate_file_infection
from django_cryptography.fields import encrypt

# Create your models here.
class User(AbstractUser):
    type = models.CharField(max_length=10,choices=(("Patient","Patient"),("Doctor","Doctor"),("Donor","Donor"),("Pharmacy","Pharmacy")))
    def __str__(self):
        return self.username

class Contact(models.Model):
    name = encrypt(models.CharField(max_length=100))
    email = encrypt(models.EmailField())
    phone = encrypt(models.BigIntegerField())
    message = encrypt(models.CharField(max_length=2048))

class SiteAnnouncement(models.Model):
    message=models.CharField(max_length=2048)
    link_exist = models.BooleanField()
    link = models.CharField(max_length=2048,blank=True,null=True)

class NotifySlot(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    pincode = models.IntegerField()
    state_id = models.IntegerField()
    district_id = models.IntegerField()

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    address1 = models.CharField(max_length=1000)
    address2 = models.CharField(max_length=1000)
    street =  models.CharField(max_length=1000)
    city = models.CharField(max_length=1000)
    state = models.CharField(max_length=1000)
    pincode = models.IntegerField()
    covid = models.BooleanField()
    skype = models.CharField(blank=True,max_length=200)
    mobile = models.BigIntegerField(null=True)

class ContactAdmin(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    heading = models.CharField(max_length=100)
    message = models.CharField(max_length=2048)