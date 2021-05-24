from django.shortcuts import render,redirect
from pharmacy.models import Medicine,Order
from django.contrib import messages
from patient.models import Bill

# Create your views here.
def searchMedicine(request):
    if request.user.type!="Doctor":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/') 
    obj = Medicine.objects.all()
    return render(request,"Doctor/searchMedicine.html",{'obj':obj,'len':len(obj)})

def filterMedicine(request):
    if request.user.type!="Doctor":
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
    return render(request,"Doctor/searchMedicine.html",{'obj':obj,'len':len(obj)})

def placeOrder(request,mid):
    if request.user.type!="Doctor":
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
    if request.user.type!="Doctor":
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
    return render(request,"Doctor/yourOrder.html",{'pending':pending,'accepted':accepted,'rejected':rejected,'shipped':shipped,'cancelled':cancelled,
                        'pl':p_l,'rl':r_l,'al':a_l,'sl':s_l,'cl':c_l})

def cancelOrder(request,oid):
    if request.user.type!="Doctor":
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