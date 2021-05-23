from django.db import models
from django.contrib.auth.models import AbstractUser
from django_clamd.validators import validate_file_infection
from django_cryptography.fields import encrypt

# Create your models here.
class User(AbstractUser):
    type = models.CharField(max_length=10,choices=(("Patient","Patient"),("Doctor","Doctor"),("Donor","Donor"),("Pharmacy","Pharmacy")))

class Contact(models.Model):
    name = encrypt(models.CharField(max_length=100))
    email = encrypt(models.EmailField())
    phone = encrypt(models.BigIntegerField())
    message = encrypt(models.CharField(max_length=2048))

class SiteAnnouncement(models.Model):
    message=models.CharField(max_length=2048)
    link_exist = models.BooleanField()
    link = models.CharField(max_length=2048,blank=True,null=True)
