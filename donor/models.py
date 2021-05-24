from django.db import models
from base.models import User
# Create your models here.
class PlasmaProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    days_covid_negative = models.IntegerField()
    plasma_last_donated = models.IntegerField(default=0)
    blood_group = models.CharField(choices=(('A+','A+'),('A-','A-'),('B+','B+'),('B-','B-'),('AB+','AB+'),('AB-','AB-'),('O+','O+'),('O-','O-')),max_length=4)
    photo = models.ImageField(upload_to = 'plasma_donors',blank=True)
    
class DonorRequest(models.Model):
    patient = models.ForeignKey(User,on_delete=models.CASCADE,related_name='patients')
    donor = models.ForeignKey(User,on_delete=models.CASCADE,related_name='donors')
    status = models.CharField(choices = (("Pending","Pending"),("Accepted","Accepted"),("Rejected","Rejected")),max_length=20,default="Pending")
    