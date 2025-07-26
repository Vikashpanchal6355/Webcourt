import os
from urllib import response
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib import auth,messages
from django.core.files.storage import FileSystemStorage
from client.models import *
from webcourt import settings
from django.db import IntegrityError
from staff.models import *
from .models import *




# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken')
                return redirect(register)
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already taken')
                return redirect(register)
            else:
                user = User.objects.create_user(username=username, password=password,email=email)
                user.save()
                return redirect('/myadmin/login')

        else:
            messages.info(request, 'Both passwords are not matching')
            return redirect(register)
    else:
        return render(request, 'myadmin/registeration.html')



def login(request):
    context = {}
    return render(request, 'myadmin/login.html', context)


def login_check(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        result = auth.authenticate(username=username, password=password)
       

        if result is None:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('/myadmin/login')
        
        
        else:
            auth.login(request, result)
            return redirect('/myadmin/dashboard')
    else:
        return redirect('/myadmin/login') 



def dashboard(request):
    context = {}
    return render(request, 'myadmin/dashboard.html',context)

def logout_user(request):
    auth.logout(request)
    return redirect('/myadmin/login')

def addstaff(request):
    context = {}
    return render(request, 'myadmin/addstaff.html',context)


def store_staff(request):
    if request.method == 'POST':
        myfname = request.POST['fname']
        mylname = request.POST['lname']
        myemail = request.POST['email']
        myusername = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        mydob=request.POST['dob']
        myeducation=request.POST['education']
        myphone = request.POST['phone']
        mygender = request.POST['gender']
        myaddress = request.POST['address']

        # Check if the username already exists
        if User.objects.filter(username=myusername).exists():
            messages.info(request, 'Username is already taken')
            return redirect('/myadmin/addstaff/')

        if password == cpassword:
            user = User.objects.create_user(first_name=myfname, last_name=mylname, email=myemail, username=myusername, password=password)
            Staff.objects.create(phone=myphone, address=myaddress, gender=mygender,dob=mydob,education=myeducation, user_id=user.id)
            return redirect('/myadmin/addstaff/')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('/myadmin/addstaff/')  
    else:
        return redirect('/myadmin/addstaff/')

def allstaff(request):
    staff = Staff.objects.all()
    context = {'staff': staff}
    return render(request, 'myadmin/allstaff.html', context)


def edit_staff(request,id):
    result = Staff.objects.get(pk=id)
    context = {'result':result}
    return render(request, 'myadmin/editstaff.html',context)



def update_staff(request,id):
    myfname = request.POST['fname']
    mylname = request.POST['lname']
    myemail = request.POST['email']
    myusername = request.POST['username']
    myphone = request.POST['phone']
    mygender  = request.POST['gender']
    myaddress = request.POST['address']
   

    user = User.objects.update_or_create(pk=id,defaults={'first_name':myfname,'last_name':mylname,'email':myemail,'username':myusername})

    Staff.objects.update_or_create(pk=id,defaults={'phone':myphone,'address':myaddress,'gender':mygender})
    return redirect('/myadmin/editstaff')

# def update_staff(request, id):
#     if request.method == 'POST':
#         myfname = request.POST['fname']
#         mylname = request.POST['lname']
#         myemail = request.POST['email']
#         myusername = request.POST['username']
#         myphone = request.POST['phone']
#         mygender = request.POST['gender']
#         myaddress = request.POST['address']
#         myeducation = request.POST['education']

#         # Retrieve the existing Staff object
#         staff = Staff.objects.get(pk=id)
        
#         # Update the related User object
#         user = staff.user
#         user.first_name = myfname
#         user.last_name = mylname
#         user.email = myemail
#         user.username = myusername
#         user.save()

#         # Update the Staff object
#         staff.phone = myphone
#         staff.gender = mygender
#         staff.address = myaddress
#         staff.education = myeducation
#         staff.save()

#         return redirect('/myadmin/allstaff/')
#     else:
#         return redirect('/myadmin/allstaff/')


def delete_staff(request,id):
    result = Staff.objects.get(pk=id)
    result.delete()
    return redirect('/myadmin/allstaff')

def addclient(request):
    context = {}
    return render(request, 'myadmin/addclient.html',context)

def store_client(request):
    if request.method == 'POST':
        myfname = request.POST['fname']
        mylname = request.POST['lname']
        myemail = request.POST['email']
        myusername = request.POST['username']
        mymname=request.POST['mname']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        mycontact = request.POST['contact']
        mygender  = request.POST['gender']
        myaddress = request.POST['address']
        
        if password == cpassword:
            if User.objects.filter(username=myusername).exists():
                messages.info(request, 'Username is already taken')
                return redirect('/myadmin/addclient/')
            elif User.objects.filter(email=myemail).exists():
                messages.info(request, 'Email is already taken')
                return redirect('/myadmin/addclient/')
            else:
                user = User.objects.create_user(first_name=myfname,last_name=mylname,email=myemail,username=myusername,password=password)
                Client.objects.create(contact=mycontact,address=myaddress,gender=mygender,user_id=user.id,middle_name=mymname)
                return redirect('/myadmin/addclient/')

        else:
            messages.info(request, 'Passwords do not match')
            return redirect('/myadmin/addclient/')

    else:
        print('Password and confirm password mismatched')


def allclient(request):
    client = Client.objects.all()
    context = {'client': client}
    return render(request, 'myadmin/allclient.html',context)

def delete_client(request,id):
    result = Client.objects.get(pk=id)
    result.delete()
    return redirect('/myadmin/allclient')



def addcases(request):
    clients = Client.objects.all()
    staffs = Staff.objects.all()
    context = {'client':clients,'staff':staffs}
    return render(request, 'myadmin/add_case.html',context)


def allcases(request):
    case = Case.objects.all()
    context = {'case': case}
    return render(request, 'myadmin/allcases.html',context)

def store_case(request):
    mytitle = request.POST['case_title']
    mydescription = request.POST['description']
    mycrimetype = request.POST['type']
    myfir_date = request.POST['fir_date']
    myfir_station = request.POST['fir_station']
    myfir_copy = request.FILES['fir_copy']
    myclient = request.POST['client']
    mystaff = request.POST['staff']

    # myfir_copy = request.FILES.get('fir_copy') 
    if myfir_copy:
        mylocation = os.path.join(settings.MEDIA_ROOT, 'copy')
        obj = FileSystemStorage(location=mylocation)
        obj.save(myfir_copy.name, myfir_copy)
    else:
        myfir_copy = None

    messages.success(request, 'Case has been successfully stored.')
    Case.objects.create(case_title=mytitle,description=mydescription,crimetype=mycrimetype,fir_date=myfir_date,fir_station=myfir_station,fir_copy=myfir_copy,client_id=myclient,staff_id=mystaff)
 
    return redirect('/myadmin/addcases/')

def edit_case(request, id): 
    # staff_id = Staff.objects.get(user_id=request.user.id)
    result = Case.objects.all()
    case = Case.objects.get(pk=id) 
    context = {'result': result, 'case': case}
    return render(request, 'myadmin/edit_case.html', context)

def update_case(request, id):
    if request.method == 'POST':
        mytitle = request.POST['case_title']
        mydescription = request.POST['description']
        mycrimetype = request.POST['type']
        myfir_date = request.POST['fir_date']
        myfir_station = request.POST['fir_station']
       
        # Check if a new FIR copy is uploaded
        myfir_copy = request.FILES.get('fir_copy', None)
        if myfir_copy:
            # Save the new FIR copy file
            mylocation = os.path.join(settings.MEDIA_ROOT, 'copy')
            obj = FileSystemStorage(location=mylocation)
            myfir_copy_path = obj.save(myfir_copy.name, myfir_copy)
        else:
            # If no new file is uploaded, keep the old one
            case = Case.objects.get(pk=id)  # Get the specific case instance
            myfir_copy_path = case.fir_copy  # Use the existing FIR copy path

        # Update the case object with the new data
        case = Case.objects.get(pk=id)  # Get the specific case instance
        case.case_title = mytitle
        case.description = mydescription
        case.crimetype = mycrimetype
        case.fir_date = myfir_date
        case.fir_station = myfir_station
        case.fir_copy = myfir_copy_path
        case.save()  # Save the instance
        messages.success(request, 'Case has been successfully updated.')

        # Redirect to the desired page
        return redirect('/myadmin/allcases/')

def view_cases(request, id):
    result3 = Case.objects.get(id=id)
    context = {'result3':result3}
    return render(request, 'myadmin/viiew_case.html', context)

def add_evidence(request, id):
    case = Case.objects.get(pk=id)
    context = {'case': case}
    return render(request, 'myadmin/add_evidence.html', context)

# def store_evidence(request, id):
#     case = Case.objects.get(pk=id)
#     myevidence = request.FILES['evidence']
#     mydescription = request.POST['description']

#     Evidence.objects.create(case=case, evidence=myevidence, description=mydescription)
#     messages.success(request, 'Evidence has been successfully stored.')
#     return redirect('/myadmin/allcases')

# def view_evidence(request, id):
#     case = Case.objects.get(pk=id)
#     evidence = Evidence.objects.filter(case=case)
#     context = {'case': case, 'evidence': evidence}
#     return render(request, 'myadmin/view_evidence.html', context)

# def delete_evidence(request, id):
#     result = Evidence.objects.get(pk=id)
#     result.delete()
#     return redirect('/myadmin/allcases')

def delete_case(request,id):
    result = Case.objects.get(pk=id)
    result.delete()
    return redirect('/myadmin/allcases')

def all_dates(request):
    result1 = Client.objects.all()
    result = Hearing.objects.all()
    context = {'result':result,'result1':result1}
    return render(request,'myadmin/hearingdate.html',context)

def delete_hearing(request,id):
    result = Hearing.objects.get(pk=id)
    result.delete()
    return redirect('/myadmin/hearingdate')

def appointment(request):
    result = Appointment.objects.all()
    context = {'result':result}
    
    return render(request, 'myadmin/appointment.html',context)

def inquiries(request):
    result1 = Client.objects.all()
    result = Contact.objects.all()
    context = {'result':result,'result1':result1}
    return render(request, 'myadmin/inquiries.html', context)

def delete_inquiries(request,id):
    result = Contact.objects.get(pk=id)
    result.delete()
    return redirect('/myadmin/inquiries')


def feedback(request):
    result = Feedback.objects.all()
    context = {'result':result}
    return render(request, 'myadmin/feedback.html',context)