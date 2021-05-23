from django.db import models
from base.models import User
# Create your models here.
class Bill(models.Model):
    amount = models.IntegerField()
    description = models.CharField(max_length=2048)
    user = models.ForeignKey(User,on_delete=models.CASCADE)