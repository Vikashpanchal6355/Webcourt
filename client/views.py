from django.shortcuts import redirect, render
from django.contrib import auth,messages
from django.contrib.auth.models import *
from client.models import *
from myadmin.models import *
from staff.models import *
from django.contrib.auth.models import *

# Create your views here.
def dashboard(request):
    context = {}
    return render(request, 'client/dashboard.html',context)

def about(request):
    context = {}
    return render(request, 'client/about.html',context)

def login(request):
    context = {}
    return render(request, 'client/login.html',context)


def login_check(request):
    username = request.POST['username']
    password = request.POST['password']


    result = auth.authenticate(username=username,password=password)

    if result is None:
         
        return redirect('/client/login')

    else:
        auth.login(request,result)
        return redirect('/client/dashboard')


def logout(request):
    auth.logout(request)
    return redirect('/client/login')

def appointment(request):
    result = Client.objects.all()
    context = {'result': result}
    return render(request, 'client/appointment.html',context)

def profile(request):
    client = Client.objects.all()
    context = {'client': client}
    return render(request, 'client/profile.html',context)



def feedback(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        feedback = Feedback(name=name, email=email, message=message)
        feedback.save()
        messages.success(request, 'Feedback sent successfully!')
        return redirect('/client/feedback')

    context = {}
    return render(request, 'client/feedback.html', context)

def contact(request):
    if request.method == 'POST':
        cname = request.POST['name']
        cemail = request.POST['email']
        csubject = request.POST['subject']
        cmessage = request.POST['message']

        contact= Contact(name=cname, email=cemail, subject=csubject, message=cmessage)
        contact.save()
        messages.success(request, 'Thank you for contacting us! Our lawyer will contact you soon.')
        return redirect('/client/contact')
    context = {}
    return render(request, 'client/contact.html',context)



def appointment_store(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        description = request.POST['description']
        # client_id = request.POST['client_id']

        store_appointment = Appointment(subject=subject, description=description)
        store_appointment.save()
        
        return redirect('/client/appointment')

    context = {}
    return render(request, 'client/appointment', context)


def case(request):
    id = request.user.id
    client = Client.objects.get(user_id=id)  
    result = Case.objects.filter(client_id=client.id)
    # hear = Hearing.objects.filter(case_id=id)
    hear=Hearing.objects.all()
    context = {'result': result,'hear':hear}
    return render(request, 'client/case.html', context)
