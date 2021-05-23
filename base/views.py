from django.shortcuts import render,redirect
from django.core.mail import send_mail
import random
from django.contrib.auth.hashers import make_password
from .models import SiteAnnouncement
from django.contrib import messages,auth
from django.contrib.auth import authenticate
from .models import Contact, User

# Create your views here.
def home(request):
    announcement = SiteAnnouncement.objects.all()
    return render(request,"home.html",{'announcement':announcement})

def contact(request):
        if request.method=="POST":
            name=request.POST["cust_name"]
            email=request.POST["cust_email"]
            phone=request.POST["cust_mobile"]
            message=request.POST["cust_message"]
            Contact.objects.create(name=name,email=email,phone=phone,message=message)
            storage = messages.get_messages(request)
            storage.used = True
            msg = 'Mr. '+name+',\n\n\tThank you for joining with our Team. We will contact you soon'
            try:
                send_mail("SaveLife Volunteer",msg,from_email='adityaintern11@gmail.com',recipient_list=[email])
            except Exception as e:
                print(e)
                messages.info(request,"Couldn't process your request now. Kindly try again later")
            else:
                messages.info(request,'Thank you for the request. Our Team will contact you soon')
        return redirect('/')

def register(request):
    if request.method=="POST":
        first_name = request.POST["first_name"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        type = request.POST["type"]
        cnfpassword = request.POST["cnfpassword"]
        if password!=cnfpassword:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Password Not Matching')
            return redirect('/')     
        obj = User.objects.filter(username=username)
        if len(obj)>0:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'User Already Exists')
            return redirect('/')     
        else:
            User.objects.create_user(first_name=first_name,email=email,username=username,password=password,type=type)
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'User Registration Successful')
            return redirect('/') 
    else:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Invalid Request')
        return redirect('/') 
        
def login(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        obj = authenticate(username=username,password=password)
        print(obj)
        if obj is not None:
            auth.login(request,obj)
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'User Login Successfully')
            return redirect('/dashboard') 
        else:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Invalid Credentials')
    return redirect('/')

def logout(request):
    auth.logout(request)
    storage = messages.get_messages(request)
    storage.used = True
    messages.info(request,'Logged Out Successfully')
    return redirect('/')

def changePassword(request):
    if request.method=="POST":
        username=request.POST["username"]
        obj = User.objects.get(username=username)
        number = random.randint(1000,9999)
        request.session["username"]=username
        request.session["otp_send"]=number
        msg = 'Hi '+obj.first_name+',\n\n\tOTP To change password: '+str(number)
        send_mail("Savelife - Password Change",msg,from_email='adityaintern11@gmail.com',recipient_list=[obj.email])
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'OTP Shared to your email id')
        return redirect('/validateOtp')
    return render(request,"startRecovery.html")

def validateOtp(request):
    if request.method=="POST":
        otp = request.POST["otp"]
        if int(otp)==int(request.session["otp_send"]):
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'OTP Verified. Provide New Password Credentials')
            return redirect('/setNewPassword')
        else:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'OTP Verification failed. Re-enter the username')
            return redirect('/changePassword')
    return render(request,'validateOtp.html')

def setNewPassword(request):
    if request.method=="POST":
        password=request.POST["new_password"]
        cnf_password=request.POST["cnf_password"]
        if password==cnf_password:
            password=make_password(password)
            obj = User.objects.get(username=request.session["username"])
            obj.password=password
            obj.save()
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Password Changed Successfully')
            return redirect('/')
        else:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Passwords not matching')
            return redirect('/setNewPassword')
    return render(request,'setNewPassword.html')

def dashboard(request):
    if request.user.type=="Doctor":
        return redirect('/doctor/dashboard')
    elif request.user.type=="Patient":
        return redirect('/patient/dashboard')
    elif request.user.type=="Donor":
        return redirect('/donor/dashboard')
    elif request.user.type=="Pharmacy":
        return redirect('/pharmacy/dashboard')