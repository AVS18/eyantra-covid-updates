from django.contrib import admin
from .models import ContactAdmin, User, SiteAnnouncement, Contact, NotifySlot
# Register your models here.
class UserRef(admin.ModelAdmin):
    list_display = ['username','first_name','email']
    list_filter = ['type']

admin.site.register(User,UserRef)

class SiteAnnRef(admin.ModelAdmin):
    list_display = ['message','link']
    list_filter = ['link']

admin.site.register(SiteAnnouncement,SiteAnnRef)

class ContactRef(admin.ModelAdmin):
    list_display = ['name','email','phone','message']

admin.site.register(Contact,ContactRef)

class NotifySlotRef(admin.ModelAdmin):
    list_display = ['user','pincode','state_id','district_id']
    list_filter = ['pincode','state_id','district_id']

admin.site.register(ContactAdmin)