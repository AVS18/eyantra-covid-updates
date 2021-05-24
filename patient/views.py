from django.shortcuts import render,redirect
from pharmacy.models import Medicine,Order
from django.contrib import messages
from .models import Bill,MedicalReport,Report
from doctor.models import Appointment, DoctorProfile,Consultation
from base.models import User
from donor.models import PlasmaProfile,DonorRequest

# Create your views here.
def searchMedicine(request):
    if request.user.type!="Patient":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/') 
    obj = Medicine.objects.all()
    return render(request,"Patient/searchMedicine.html",{'obj':obj,'len':len(obj)})

def filterMedicine(request):
    if request.user.type!="Patient":
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
    return render(request,"Patient/searchMedicine.html",{'obj':obj,'len':len(obj)})

def placeOrder(request,mid):
    if request.user.type!="Patient":
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
    if request.user.type!="Patient":
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
    return render(request,"Patient/yourOrder.html",{'pending':pending,'accepted':accepted,'rejected':rejected,'shipped':shipped,'cancelled':cancelled,
                        'pl':p_l,'rl':r_l,'al':a_l,'sl':s_l,'cl':c_l})

def cancelOrder(request,oid):
    if request.user.type!="Patient":
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

def yourMedicalReport(request):
    if request.user.type!="Patient":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/')
    if request.method=="POST":
        obj =  MedicalReport.objects.filter(patient=request.user).select_related()
        spo2 = request.POST["spo2"]
        bp = request.POST["bp"]
        sugar = request.POST["sugar"]
        covid = request.POST["covid"]
        if len(obj)==0:
            MedicalReport.objects.create(patient=request.user,spo2=spo2,bp=bp,sugar=sugar,covid=covid)
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Report Created Successfully')
            return redirect('/dashboard')
        else:
            obj[0].spo2 = spo2
            obj[0].bp = bp
            obj[0].sugar = sugar
            obj[0].covid = covid
            obj[0].save()
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Report Updated Successfully')
            return redirect('/dashboard')
    current_report = MedicalReport.objects.filter(patient=request.user).select_related()
    if len(current_report)==0:
        return render(request,"Patient/yourMedicalReport.html")
    else:
        return render(request,"Patient/yourMedicalReport.html",{'report':current_report[0]})

def attachReport(request):
    if request.user.type!="Patient":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/')
    if request.method=="POST":
        myfiles = request.FILES
        file = myfiles["file"]
        description = request.POST["description"]
        obj = Report.objects.create(user=request.user,file=file,description=description)
        reports = MedicalReport.objects.filter(patient=request.user)
        reports[0].report.add(obj)
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Document Saved Successfully')
        return redirect('/patient/MedicalReport')
    storage = messages.get_messages(request)
    storage.used = True
    messages.info(request,'Invalid Request')
    return redirect('/dashboard')
        
def viewDoctor(request):
    if request.user.type!="Patient":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/')
    
    doctors = DoctorProfile.objects.all()
    return render(request,'Patient/viewDoctors.html',{'doctor':doctors})

def bookAppointment(request,did):
    if request.user.type!="Patient":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/')
    
    doctor = User.objects.get(id=did)
    patient = request.user
    report = MedicalReport.objects.filter(patient=request.user)
    if len(report)==0:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'First Fill your medical reports and then book appointment')
        return redirect('/dashboard')
    obj = Appointment.objects.filter(doctor=doctor,patient=patient)
    if len(obj)==0:
        Appointment.objects.create(doctor=doctor,patient=patient,status="Pending")
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Appointment Created Successfully')
        return redirect('/dashboard')
    else:
        obj[0].status = "Pending"
        obj[0].save()
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Appointment Updated Successfully')
        return redirect('/dashboard')

def viewAppointment(request):
    if request.user.type!="Patient":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/')
    
    pending = Appointment.objects.filter(patient=request.user,status="Pending")
    open = Appointment.objects.filter(patient=request.user,status="Open")
    close = Appointment.objects.filter(patient=request.user,status="Close")
    pl,ol,cl = len(pending),len(open),len(close)
    return render(request,"Patient/displayAppointment.html",{'pending':pending,'open':open,'close':close, 'pl':pl,'ol':ol,'cl':cl})

def viewConsultation(request,cid):
    if request.user.type!="Patient":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/') 
    consultation = Consultation.objects.get(id=cid)
    medical_history = MedicalReport.objects.filter(patient=consultation.appointment.patient)
    return render(request,"Patient/viewConsultation.html",{'consultation':consultation,'medhist':medical_history[0]})

def yourBill(request):
    if request.user.type!="Patient":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/') 
    
    bill = Bill.objects.filter(user=request.user)
    return render(request,"Patient/bill.html",{'bill':bill})

def searchDonors(request):
    if request.user.type!="Patient":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/') 
    obj = PlasmaProfile.objects.all()
    return render(request,"Patient/searchDonors.html",{'obj':obj,'len':len(obj)})

def filterDonors(request):
    if request.user.type!="Patient":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/') 
    days_covid_negative = request.GET.get('days_covid_negative')
    plasma_last_donated = request.GET.get('plasma_last_donated')
    blood_group = request.GET.get('blood_group')
    obj = None
    if days_covid_negative != '':
        if plasma_last_donated != '':
            if blood_group != '':
                obj = PlasmaProfile.objects.filter(plasma_last_donated__gte=plasma_last_donated,days_covid_negative__gte=days_covid_negative,blood_group=blood_group)
            else:
                obj = PlasmaProfile.objects.filter(plasma_last_donated__gte=plasma_last_donated,days_covid_negative__gte=days_covid_negative)
        else:
            if blood_group != '':
                obj = PlasmaProfile.objects.filter(days_covid_negative__gte=days_covid_negative,blood_group=blood_group)
            else:
                obj = PlasmaProfile.objects.filter(days_covid_negative__gte=days_covid_negative)
    else:
        if plasma_last_donated != '':
            if blood_group != '':
                obj = PlasmaProfile.objects.filter(plasma_last_donated__gte=plasma_last_donated,blood_group=blood_group)
            else:
                obj = PlasmaProfile.objects.filter(plasma_last_donated__gte=plasma_last_donated)
        else:
            if blood_group != '':
                obj = PlasmaProfile.objects.filter(blood_group=blood_group)
    return render(request,"Patient/searchDonors.html",{'obj':obj,'len':len(obj)})

def requestDonor(request,did):
    if request.user.type!="Patient":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/') 
    
    donor = User.objects.get(id=did)
    if donor.type!="Donor":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Invalid Donor. Try again')
        return redirect('/patient/searchDonors') 
    patient = request.user
    obj = DonorRequest.objects.filter(donor=donor,patient=patient)  
    if len(obj)!=0:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Request Already Placed')
        return redirect('/patient/searchDonors') 
    DonorRequest.objects.create(donor=donor,patient=patient,status="Pending")
    storage = messages.get_messages(request)
    storage.used = True
    messages.info(request,'Request Initiated Successfully')
    return redirect('/dashboard')

def showDonorRequest(request):
    if request.user.type!="Patient":
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Allowed. Please Re-Login')
        return redirect('/') 
    pending = DonorRequest.objects.filter(patient=request.user,status="Pending")
    accepted = DonorRequest.objects.filter(patient=request.user,status="Accepted")
    rejected = DonorRequest.objects.filter(patient=request.user,status="Rejected")
    pl,al,rl = len(pending),len(accepted),len(rejected)
    print(pending)
    return render(request,"Patient/showDonorRequest.html",{'pending':pending,'accepted':accepted,'rejected':rejected,'pl':pl,'al':al,'rl':rl})