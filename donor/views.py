from django.shortcuts import render,redirect
from pharmacy.models import Medicine,Order
from django.contrib import messages
from patient.models import Bill
from .models import PlasmaProfile
def searchMedicine(request):
    if request.user.type!="Donor":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/') 
    obj = Medicine.objects.all()
    return render(request,"Donor/searchMedicine.html",{'obj':obj,'len':len(obj)})

def filterMedicine(request):
    if request.user.type!="Donor":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/') 
    cost = request.GET.get('cost')
    delivery = request.GET.get('expected_delivery')
    name = request.GET.get('name')
    obj = None
    if cost != '':
        if delivery != '':
            if name != '':
                obj = Medicine.objects.filter(name__startswith=name,cost__lte=cost,expected_delivery__lte=delivery)
            else:
                obj = Medicine.objects.filter(cost__lte=cost,expected_delivery__lte=delivery)
        else:
            if name != '':
                obj = Medicine.objects.filter(name__startswith=name,cost__lte=cost)
            else:
                obj = Medicine.objects.filter(cost__lte=cost)
    else:
        if delivery != '':
            if name != '':
                obj = Medicine.objects.filter(name__startswith=name,expected_delivery__lte=delivery)
            else:
                obj = Medicine.objects.filter(expected_delivery__lte=delivery)
        else:
            if name != '':
                obj = Medicine.objects.filter(name__startswith=name)
    return render(request,"Donor/searchMedicine.html",{'obj':obj,'len':len(obj)})

def placeOrder(request,mid):
    if request.user.type!="Donor":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/') 
    
    medicine_obj = Medicine.objects.get(id=mid)
    ordered_by = request.user
    ordered_to = medicine_obj.user
    status = "Pending"
    description = "Purchased "+medicine_obj.name+" from "+medicine_obj.user.first_name
    amount = medicine_obj.cost
    bill = Bill.objects.create(user=request.user,amount=amount,description=description)        
    obj = Order.objects.create(medicine = medicine_obj, ordered_by = ordered_by, ordered_to = ordered_to,status=status,billing=bill)
    storage = messages.get_messages(request)
    storage.used = True
    messages.info(request,'Order Placed Successfully')
    return redirect('/dashboard')
    
def yourOrder(request):
    if request.user.type!="Donor":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/') 

    pending = Order.objects.filter(ordered_by = request.user,status="Pending")
    accepted = Order.objects.filter(ordered_by = request.user,status="Accepted")
    rejected = Order.objects.filter(ordered_by = request.user,status="Rejected")
    shipped = Order.objects.filter(ordered_by = request.user,status="Shipped")
    cancelled = Order.objects.filter(ordered_by = request.user,status="Cancelled")
    p_l,a_l,r_l,s_l,c_l = len(pending),len(accepted),len(rejected),len(shipped),len(cancelled)
    return render(request,"Donor/yourOrder.html",{'pending':pending,'accepted':accepted,'rejected':rejected,'shipped':shipped,'cancelled':cancelled,
                        'pl':p_l,'rl':r_l,'al':a_l,'sl':s_l,'cl':c_l})

def cancelOrder(request,oid):
    if request.user.type!="Donor":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/') 

    order = Order.objects.get(id=oid)
    bill = Bill.objects.get(id = order.billing.id)
    bill.amount = int(0.25*bill.amount)
    bill.description +="-Cancelled"
    bill.save()
    order.status="Cancelled"
    order.save()
    storage = messages.get_messages(request)
    storage.used = True
    messages.info(request,'Order Cancelled Successfully')
    return redirect('/dashboard')

def addDonorProfile(request):
    if request.user.type!="Donor":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/') 

    if request.method=="POST":
        days_covid_negative = request.POST["days_covid_negative"]
        plasma_last_donated = request.POST["plasma_last_donated"]
        blood_group = request.POST["blood_group"]
        obj = PlasmaProfile.objects.filter(user=request.user)
        myfiles = request.FILES
        photo = myfiles["photo"]
        if len(obj)==0:
            PlasmaProfile.objects.create(user=request.user,days_covid_negative=days_covid_negative,plasma_last_donated=plasma_last_donated,blood_group=blood_group,photo=photo)
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Profile Created Successfully')
            return redirect('/dashboard')
        else:
            obj[0].days_covid_negative = days_covid_negative
            obj[0].plasma_last_donated = plasma_last_donated
            obj[0].blood_group = blood_group
            obj[0].save()
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Profile Updated Successfully')
            return redirect('/dashboard')
    profile = PlasmaProfile.objects.filter(user=request.user)
    if len(profile)==0:
        return render(request,"Donor/addDonorProfile.html")
    else:
        return render(request,"Donor/addDonorProfile.html",{'profile':profile[0]})
