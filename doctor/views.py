from doctor.models import Appointment, Consultation, CovidTips, DoctorProfile, Medicines
from django.shortcuts import render,redirect
from pharmacy.models import Order,Medicine
from django.contrib import messages
from patient.models import Bill
from patient.models import MedicalReport
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

def addDoctorProfile(request):
    if request.user.type!="Doctor":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/') 

    if request.method=="POST":
        experience = request.POST["experience"]
        specialization = request.POST["specialization"]
        working_at = request.POST["working_at"]
        obj = DoctorProfile.objects.filter(user=request.user)
        myfiles = request.FILES
        photo = myfiles["photo"]
        if len(obj)==0:
            DoctorProfile.objects.create(user=request.user,experience=experience,specialization=specialization,working_at=working_at,photo=photo)
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Profile Created Successfully')
            return redirect('/dashboard')
        else:
            obj[0].experience = experience
            obj[0].specialization = specialization
            obj[0].working_at = working_at
            obj[0].save()
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Profile Updated Successfully')
            return redirect('/dashboard')
    profile = DoctorProfile.objects.filter(user=request.user)
    if len(profile)==0:
        return render(request,"Doctor/addDoctorProfile.html")
    else:
        return render(request,"Doctor/addDoctorProfile.html",{'profile':profile[0]})

def viewAppointment(request):
    if request.user.type!="Doctor":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/')
    
    pending = Appointment.objects.filter(doctor=request.user,status="Pending")
    open = Appointment.objects.filter(doctor=request.user,status="Open")
    close = Appointment.objects.filter(doctor=request.user,status="Close")
    pl,ol,cl = len(pending),len(open),len(close)
    return render(request,"Doctor/viewAppointments.html",{'pending':pending,'open':open,'close':close, 'pl':pl,'ol':ol,'cl':cl})

def openAppointment(request,aid):
    if request.user.type!="Doctor":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/') 
    try:
        obj = Appointment.objects.get(id = aid)
        obj.status = "Open"
        obj.save()
        consultation = Consultation.objects.filter(appointment=obj)
        if len(consultation)!=0:
            consultation[0].status="Open"
            consultation[0].save()
        else:
            Consultation.objects.create(appointment=obj)
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Appointment Opened Successfully')
        return redirect('/dashboard') 
    except Exception as e:
        print(e)
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Something went wrong')
        return redirect('/') 

def closeAppointment(request,aid):
    if request.user.type!="Doctor":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/') 
    try:
        obj = Appointment.objects.get(id = aid)
        obj.status = "Close"
        obj.save()
        description = "Doctor "+obj.doctor.first_name+" consulation fees"
        bill = Bill.objects.create(user=obj.patient,amount=250,description=description)        
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Appointment Close Successfully')
        return redirect('/dashboard') 
    except Exception:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Something went wrong')
        return redirect('/') 

def editConsultation(request,cid):
    if request.user.type!="Doctor":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/') 
    consultation = Consultation.objects.get(id=cid)
    if consultation.appointment.doctor != request.user:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,"You can't edit others consultation")
        return redirect('/dashboard') 
    old_consultation = Consultation.objects.filter(appointment__patient=consultation.appointment.patient).exclude(appointment__doctor=consultation.appointment.doctor)
    medical_history = MedicalReport.objects.filter(patient=consultation.appointment.patient)
    ocl = len(old_consultation)
    return render(request,"Doctor/editConsultation.html",{'consultation':consultation,'oldcon':old_consultation,'medhist':medical_history[0],'ocl':ocl})

def viewConsultation(request,cid):
    if request.user.type!="Doctor":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/') 
    consultation = Consultation.objects.get(id=cid)
    medical_history = MedicalReport.objects.filter(patient=consultation.appointment.patient)
    return render(request,"Doctor/viewConsultation.html",{'consultation':consultation,'medhist':medical_history[0]})

def addMedicine(request):
    if request.method=="POST":
        cid = request.POST["cid"]
        name = request.POST["name"]
        dosage = request.POST["dosage"]
        medicine = Medicines.objects.create(name=name,dosage=dosage,added_by=request.user)
        consultation = Consultation.objects.get(id=cid)
        consultation.medicines.add(medicine)
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Medicine Added Successfully')
        return redirect('/doctor/editConsultation/'+str(cid))
    storage = messages.get_messages(request)
    storage.used = True
    messages.info(request,'Invalid Request')
    return redirect('/')

def rejectAppointment(request,aid):
    if request.user.type!="Doctor":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/') 
    try:
        obj = Appointment.objects.get(id = aid)
        obj.status = "Close"
        obj.save()
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Appointment Close Successfully')
        return redirect('/dashboard') 
    except Exception:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Something went wrong')
        return redirect('/') 

def addTips(request):
    if request.user.type!="Doctor":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/') 
    if request.method=="POST":
        title = request.POST["title"]
        description = request.POST["description"]
        CovidTips.objects.create(title=title,description=description,user=request.user) 
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Covid Tip Added Successfully')
        return redirect('/dashboard') 
    obj = CovidTips.objects.filter(user=request.user)
    return render(request,"Doctor/addTip.html",{'obj':obj})