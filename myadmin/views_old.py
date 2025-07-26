import os
from urllib import response
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib import auth,messages
from django.core.files.storage import FileSystemStorage
from webcourt import settings
from .models import *
from django.db import IntegrityError




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
        myphone = request.POST['phone']
        mygender = request.POST['gender']
        myaddress = request.POST['address']

        # Check if the username already exists
        if User.objects.filter(username=myusername).exists():
            messages.info(request, 'Username is already taken')
            return redirect('/myadmin/addstaff/')

        if password == cpassword:
            user = User.objects.create_user(first_name=myfname, last_name=mylname, email=myemail, username=myusername, password=password)
            Staff.objects.create(phone=myphone, address=myaddress, gender=mygender, user_id=user.id)
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


def editstaff(request):
  context = {}
  return render(request, 'myadmin/editstaff.html', context)

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
                Client.objects.create(contact=mycontact,address=myaddress,gender=mygender,user_id=user.id)
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
    result = client.objects.get(pk=id)
    result.delete()
    return redirect('/myadmin/allclient.html')

def addcases(request):
    context = {}
    return render(request, 'myadmin/add_case.html',context)

from django.shortcuts import get_object_or_404, redirect

def store_case(request):
    if request.method == "POST":
        mytitle = request.POST.get('title')
        mydescription = request.POST.get('description')
        mycrimetype = request.POST.get('type')
        myfir_date = request.POST.get('fir_date')
        myfir_station = request.POST.get('fir_station')
        myclient_id = request.POST.get('client')
        mystaff_id = request.POST.get('staff')
        myfir_copy = request.FILES.get('fir_copy')

        # Fetch related objects
        myclient = get_object_or_404(Client, id=myclient_id)
        mystaff = get_object_or_404(Staff, id=mystaff_id)

        # Handle file upload
        if myfir_copy:
            mylocation = os.path.join(settings.MEDIA_ROOT, 'copy')
            file_storage = FileSystemStorage(location=mylocation)
            saved_file_path = file_storage.save(myfir_copy.name, myfir_copy)
            myfir_copy = f'copy/{saved_file_path}'

        # Create the case
        Case.objects.create(
            case_title=mytitle,
            description=mydescription,
            crimetype=mycrimetype,
            fir_date=myfir_date,
            fir_station=myfir_station,  
            fir_copy=myfir_copy,  # Ensure this field exists in your model
            client_id=myclient,      # Ensure this field exists in your model
            staff_id=mystaff        # Ensure this field exists in your model
        )

        # Redirect on success
        return redirect('/myadmin/allcases/')
    else:
        return redirect('/myadmin/addcases/')

# def store_case(request):
#     # mytitle = request.POST['case_title']
#     # mydescription = request.POST['description']
#     # mycrimetype = request.POST['type']
#     myfir_date = request.POST['fir_date']
#     myfir_station = request.POST['fir_station']
#     # myfir_copy = request.FILES['fir_copy']
#     myclient = request.POST['client']
#     mystaff = request.POST['staff']
#     if "case_title" in request.POST:
#         case_title = request.POST["case_title"]
#     if "description" in request.POST:
#         description = request.POST["description"]
#     if "crimetype" in request.POST:
#         crimetype = request.POST["crimetype"]
#     if "fir_copy" in request.FILES:
#         fir_copy = request.FILES["fir_copy"]

#     mylocation = os.path.join(settings.MEDIA_ROOT, 'copy')
#     obj = FileSystemStorage(location=mylocation)
#     obj.save(fir_copy.name,fir_copy)


#     Case.objects.create(case_title=case_title,description=description,crimetype=crimetype,fir_date=myfir_date,fir_station=myfir_station,fir_copy=fir_copy,client_id=myclient,staff_id=mystaff)
#     return redirect('/myadmin/addcases/')
# def store_case(request):
#     # Extract POST data
#     mytitle = request.POST.get('title')-
#     mydescription = request.POST.get('description')
#     mycrimetype = request.POST.get('type')
#     myfir_date = request.POST.get('fir_date')
#     myfir_station = request.POST.get('fir_station')
#     myclient = request.POST.get('client')
#     mystaff = request.POST.get('staff')

#     # Get the file safely using .get(), so it won't raise an error if missing
#     myfir_copy = request.FILES.get('fir_copy')  # This will be None if 'fir_copy' is not provided

#     # Check if required fields are provided
#     if not all([mytitle, mydescription, mycrimetype, myfir_date, myfir_station, myclient, mystaff]):
#         return redirect('/myadmin/addcases/')

#     # Handle file upload (if any)
#     if myfir_copy:
#         # Ensure file storage location is correct
#         mylocation = os.path.join(settings.MEDIA_ROOT, 'copy')
#         file_storage = FileSystemStorage(location=mylocation)
#         myfir_copy = file_storage.save(myfir_copy.name, myfir_copy)

#     # Create the case object in the database
#     try:
#         Case.objects.create(
#             title=mytitle,
#             description=mydescription,
#             crimetype=mycrimetype,
#             fir_date=myfir_date,
#             fir_station=myfir_station,
#             fir_copy=myfir_copy,  # This will be None if no file was uploaded
#             client_username=myclient,
#             staff_username=mystaff
#         )
#     except Exception as e:
#         # Log the error or handle it as necessary
#         print(f"Error creating case: {e}")
#         return redirect('/myadmin/addcases/')

#     # Redirect to case add page after success
#     return redirect('/myadmin/addcases/')

def allcases(request):
    case = Case.objects.all()
    context = {'case': case}
    return render(request, 'myadmin/allcases.html',context)


def hearingdate(request):
    context = {}
    return render(request, 'myadmin/hearingdate.html',context)

def appointment(request):
    context = {}
    return render(request, 'myadmin/appointment.html',context)

def inquiries(request):
    context = {}
    return render(request, 'myadmin/inquiries.html', context)

def feedback(request):
  context = {}
  return render(request, 'myadmin/feedback.html', context)
