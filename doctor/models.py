from django.db import models
from base.models import User
# Create your models here.
class DoctorProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    experience = models.IntegerField()
    specialization = models.CharField(max_length=200)
    working_at = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='doctor_pics',null=True)

class Appointment(models.Model):
    patient = models.ForeignKey(User,related_name='patient',on_delete=models.SET_NULL,null=True)
    doctor = models.ForeignKey(User,related_name='doctor',on_delete=models.SET_NULL,null=True)
    status = models.CharField(choices=(('Pending','Pending'),('Open','Open'),('Close','Close')),max_length=10)
    date_created = models.DateTimeField(auto_now_add=True)

class Medicines(models.Model):
    name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=200)
    added_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    added_at = models.DateTimeField(auto_now_add=True)

class Consultation(models.Model):
    appointment = models.OneToOneField(Appointment,on_delete=models.CASCADE)
    medicines = models.ManyToManyField(Medicines)
    fee = models.IntegerField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CovidTips(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    title = models.CharField(max_length=400)
    description = models.CharField(max_length=2048)
