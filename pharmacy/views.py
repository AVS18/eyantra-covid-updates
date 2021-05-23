from django.shortcuts import render,redirect
from django.core.mail import send_mail
from .models import Medicine
from django.contrib import messages

# Create your views here.
def addMedicine(request):
    if request.user.type!="Pharmacy":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/')     
    if request.method=="POST":
        name = request.POST["name"]
        description = request.POST["description"]
        cost = request.POST["cost"]
        expiry_date = request.POST["expiry_date"]
        expected_delivery = request.POST["expected_delivery"]
        myfile = request.FILES
        image = myfile["image"]
        obj = Medicine.objects.create(name=name,description=description,cost=cost,
                        expiry_date=expiry_date,expected_delivery=expected_delivery,
                        image=image,user=request.user)
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Medicine Added Successfully')
        return redirect('/dashboard')
    return render(request,"Pharmacy/addMedicine.html")

def yourMedicine(request):
    if request.user.type!="Pharmacy":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/')     
    obj = Medicine.objects.filter(user=request.user)
    return render(request,"Pharmacy/yourMedicine.html",{'obj':obj})

def updateMedicine(request,mid):
    if request.user.type!="Pharmacy":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/')     
    if request.method=="POST":
        cost = request.POST["cost"]
        expiry_date = request.POST["expiry_date"]
        expected_delivery = request.POST["expected_delivery"]
        obj = Medicine.objects.get(id=mid)
        obj.cost=cost
        obj.expiry_date = expiry_date
        obj.expected_delivery = expected_delivery
        obj.save()
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Medicine Updated Successfully')
        return redirect('/dashboard')     
    obj = Medicine.objects.get(id=mid)
    return render(request,"Pharmacy/updateMedicine.html",{'item':obj,'id':mid})

def deleteMedicine(request,mid):
    if request.user.type!="Pharmacy":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/')     
    try:
        obj= Medicine.objects.filter(id=mid).delete()
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Medicine Deleted Successfully')
        return redirect('/dashboard')
    except Exception as e:
        print(e)
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Something went wrong. Try again later')
        return redirect('/')     