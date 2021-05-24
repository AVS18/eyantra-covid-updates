from django.shortcuts import render,redirect
from django.core.mail import send_mail
from .models import Medicine,Order,Bill
from django.contrib import messages
from patient.models import Bill

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

def yourOrders(request):
    pending = Order.objects.filter(status="Pending",ordered_to=request.user)
    cancelled = Order.objects.filter(status="Cancelled",ordered_to=request.user)
    rejected = Order.objects.filter(status="Rejected",ordered_to=request.user)
    accepted = Order.objects.filter(status="Accepted",ordered_to=request.user)
    shipped = Order.objects.filter(ordered_to= request.user,status="Shipped")
    p_l,a_l,r_l,s_l,c_l = len(pending),len(accepted),len(rejected),len(shipped),len(cancelled)
    return render(request,"Pharmacy/yourOrders.html",{'pending':pending,'accepted':accepted,'rejected':rejected,'shipped':shipped,'cancelled':cancelled,
                        'pl':p_l,'rl':r_l,'al':a_l,'sl':s_l,'cl':c_l})


def acceptOrder(request,oid):
    if request.user.type!="Pharmacy":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/')     
    obj = Order.objects.get(id=oid)
    obj.status="Accepted"
    obj.save()
    storage = messages.get_messages(request)
    storage.used = True
    messages.info(request,'Order Accepted Successfully')
    return redirect('/dashboard')     

def rejectOrder(request,oid):
    if request.user.type!="Pharmacy":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/')     
    obj = Order.objects.get(id=oid)
    obj.status="Rejected"
    obj.save()
    bill_id = obj.billing.id
    Bill.objects.filter(id=bill_id).delete()
    storage = messages.get_messages(request)
    storage.used = True
    messages.info(request,'Order Rejected Successfully')
    return redirect('/dashboard')         

def shipment(request,oid):
    if request.user.type!="Pharmacy":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/') 
    if request.method=="POST":
        obj = Order.objects.get(id=oid)
        myfiles = request.FILES
        receipt = myfiles['receipt']
        service = request.POST["service"]
        tracking_id = request.POST["tracking_id"]
        obj.status = "Shipped"
        obj.receipt = receipt
        obj.service = service
        obj.tracking_id = tracking_id
        obj.save()
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Order Updated Successfully')
        return redirect('/dashboard')     
    obj = Order.objects.get(id=oid)
    return render(request,"Pharmacy/updateOrder.html",{'obj':obj})