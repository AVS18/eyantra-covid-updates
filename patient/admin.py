from django.contrib import admin
from .models import Bill,MedicalReport,Report
# Register your models here.
admin.site.register(Bill)
admin.site.register(MedicalReport)
admin.site.register(Report)