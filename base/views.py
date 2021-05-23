from django.shortcuts import render,redirect
from django.core.mail import send_mail
import random
from django.contrib.auth.hashers import make_password
from .models import NotifySlot, SiteAnnouncement,Profile
from django.contrib import messages,auth
from django.contrib.auth import authenticate
from .models import Contact, User, NotifySlot
import requests
from fake_useragent import UserAgent
import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

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
    return render(request,request.user.type+'/'+'dashboard.html')

@csrf_exempt
def cowinSlot(request):
    obj = NotifySlot.objects.filter(user=request.user)
    already = False
    if len(obj)>0:
        already=True
    temp_user_agent = UserAgent()
    if already:
        return render(request,"cowin.html",{'agent':temp_user_agent.random,'obj':obj[0],'already':already})
    else:
        return render(request,"cowin.html",{'agent':temp_user_agent.random,'already':already})

def getSlotDay(request):
    if request.method=="POST":
        date = request.POST["date"]
        pincode = request.POST["pincode"]
        temp_user_agent = UserAgent()
        headers = {
            'accept': 'application/json',
            'Accept-Language': 'hi_IN',
            'User-Agent': temp_user_agent.random
        }
        date = datetime.strptime(date, "%Y-%m-%d").strftime('%d-%m-%Y')
        params = (
            ('pincode', pincode),
            ('date', date),
        )
        response = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin', headers=headers, params=params)
        json_data = json.loads(response.text)
        return render(request,"showData.html",{'data':json_data})
    else:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Passwords not matching')
        return redirect('/dashboard')    

def getSlotWithDistrict(request):
    if request.method=="POST":
        state = request.POST["states"]
        district = request.POST["district"]
        date = request.POST["date"]
        temp_user_agent = UserAgent()
        headers = {
            'accept': 'application/json',
            'Accept-Language': 'hi_IN',
            'User-Agent': temp_user_agent.random
        }
        date = datetime.strptime(date, "%Y-%m-%d").strftime('%d-%m-%Y')
        params = (
            ('district_id', district),
            ('date', date),
        )
        response = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict', headers=headers, params=params)
        json_data = json.loads(response.text)
        return render(request,"showData.html",{'data':json_data})
    else:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Passwords not matching')
        return redirect('/dashboard')    

def notify(request):
    val = NotifySlot.objects.filter(user=request.user)
    if len(val)>0:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Already Registered for Notifications')
        return redirect('/dashboard')
    if request.method=="POST":
        pincode = request.POST["setpincode"]
        district = request.POST["setdistrict"]
        state = request.POST["setstate"]
        obj = NotifySlot.objects.create(user=request.user,pincode=pincode,district_id=district,state_id=state)
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Subscribed successfully for notifications')
        return redirect('/dashboard')
    storage = messages.get_messages(request)
    storage.used = True
    messages.info(request,'Invalid Request')
    return redirect('/dashboard')


def addProfile(request):
    if request.method=="POST":
        address1 = request.POST["address1"]
        address2 = request.POST["address2"]
        street = request.POST["street"]
        city = request.POST["city"]
        state = request.POST["state"]
        pincode = request.POST["pincode"]
        covid = request.POST["covid"]
        skype = request.POST["skype"]
        mobile = request.POST["mobile"]
        obj = Profile.objects.create(user=request.user,address1=address1,
                                address2=address2,street=street,city=city,
                                state=state,pincode=pincode,covid=covid,skype=skype,mobile=mobile)
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Profile Created Successfully')
        return redirect('/dashboard')
    obj = Profile.objects.filter(user=request.user)
    if len(obj)==0:
        return render(request,str(request.user.type)+'/'+"addProfile.html")
    else:
        return render(request,str(request.user.type)+'/'+"updateProfile.html")

def updateProfile(request):
    if request.method=="POST":
        address1 = request.POST["address1"]
        address2 = request.POST["address2"]
        street = request.POST["street"]
        city = request.POST["city"]
        state = request.POST["state"]
        pincode = request.POST["pincode"]
        covid = request.POST["covid"]
        obj = Profile.objects.get(user=request.user)
        obj.address1 = address1
        obj.address2 = address2
        obj.street = street
        obj.city = city
        obj.state = state
        obj.pincode = pincode
        obj.covid = covid
        obj.save()
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Profile Updated Successfully')
        return redirect('/dashboard')        
    storage = messages.get_messages(request)
    storage.used = True
    messages.info(request,'Invalid Request')
    return redirect('/dashboard')

        