import os
from django.conf import settings
from django.contrib.auth.models import *
from django.shortcuts import render,redirect
from django.contrib import auth,messages
from django.core.files.storage import FileSystemStorage
from myadmin.models import *
from staff.models import *

def login(request):
    context = {}
    return render(request, 'staff/login.html', context)

def login_check(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        result = auth.authenticate(username=username, password=password)
       
        if result is None:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('/staff/login') 
        
        else:
            auth.login(request, result)
            return redirect('/staff/dashboard')
    else:
        return redirect('/staff/login') 


def dashboard(request):
    context = {}
    return render(request, 'staff/dashboard.html',context)

def all_cases(request):
    id = request.user.id
    staff_id = Staff.objects.get(user_id=id)
    result = Case.objects.filter(staff_id=staff_id)
    context = {'result':result}
    return render(request,'staff/all_cases.html',context)

def case_delete(request, pk):
    case = Case.objects.get(pk=pk)
    case.delete()
    return redirect('/staff/all_cases/')

def view_cases(request, id):
    result3 = Case.objects.get(id=id)
    context = {'result3':result3}
    return render(request, 'staff/view_case.html', context)

def edit_case(request, id): 
    staff_id = Staff.objects.get(user_id=request.user.id)
    result = Case.objects.filter(staff_id=staff_id)
    case = Case.objects.get(pk=id) 
    context = {'result': result, 'case': case}
    return render(request, 'staff/edit_case.html', context)

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
        return redirect('/staff/all_cases/')
    
    case = Case.objects.get(pk=id)  # Get the specific case instance
    return render(request, 'staff/edit_case.html', {'case': case})

def add_evidence(request):
    id = request.user.id
    staff_id = Staff.objects.get(user_id=id)
    result = Case.objects.filter(staff_id=staff_id)
    context = {'result':result}
    return render(request,'staff/add_evidence.html',context)

def store_evidence(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            case_id = request.POST.get('case')
            evidence_file = request.FILES.get('evidenceFile')

            try:
                case = Case.objects.get(id=case_id)
            except Case.DoesNotExist:
                messages.error(request, "Case not found!")
                return redirect('/staff/add_evidence') 

            evidence = Evidence(case=case, file=evidence_file)
            evidence.save()
            messages.success(request, "Evidence file has been successfully uploaded.")
            return redirect('/staff/add_evidence')

    messages.error(request, "There was an error with the evidence upload.")
    return redirect('/staff/add_evidence') 


def details_evidence(request,id):
    result = Evidence.objects.filter(pk=id)
    context = {'result':result}
    return render(request,'staff/view_evidence.html',context)

def delete_evidence(request,id):
    result = Evidence.objects.get(pk=id)
    result.delete()
    return redirect('/staff/details_evidence/')

def edit_evidence(request,id):
    case = Case.objects.all()
    result = Evidence.objects.get(pk=id)
    
    context = {'result':result,'case':case}
    return render(request, 'staff/edit_evidence.html',context)

def update_evidence(request,id):
    mytitle = request.POST['title']
    mydescription = request.POST['description']
    myevidence = request.FILES['evidence']
    mycase = request.POST['case']

    mylocation = os.path.join(settings.MEDIA_ROOT, 'docs')
    obj = FileSystemStorage(location=mylocation)
    obj.save(myevidence.name,myevidence)

    Evidence.objects.update_or_create(pk=id,defaults={'title':mytitle,'description':mydescription,'evidence':myevidence,'case_id':mycase})
    return redirect('/staff/details_evidence/')

def all_evidence(request):
    id = request.user.id
    staff_id = Staff.objects.get(user_id=id)
    result = Evidence.objects.filter(case__staff_id=staff_id)
    context = {'result':result}
    return render(request,'staff/all_evidence.html',context)



def hearing(request):
    id = request.user.id
    staff_id = Staff.objects.get(user_id=id)
    result = Case.objects.filter(staff_id=staff_id)
    result1 = Client.objects.all()

    context = {'result':result,'result1':result1}
    return render(request,'staff/hearing.html',context)

def store_hearing(request):
    mydate = request.POST['ndate']
    myremarks = request.POST['remarks']
    mystatus = request.POST['status']
    mycase = request.POST['case']

    Hearing.objects.create(nextdate=mydate,remarks=myremarks,status=mystatus,case_id=mycase)
    return redirect('/staff/hearing/')

def all_hearing(request):
    id = request.user.id
    staff_id = Staff.objects.get(user_id=id)
    result = Hearing.objects.filter(case__staff_id=staff_id)
    context = {'result':result}
    return render(request,'staff/all_hearing.html',context)

def edit_hearing(request,id):
    case = Case.objects.all()
    result = Hearing.objects.get(pk=id)
    result1 = Client.objects.all()
    
    context = {'result':result,'case':case ,'result1':result1}
    return render(request, 'staff/edit_hearing.html',context)


def update_hearing(request,id):
    mydate = request.POST['ndate']
    myremarks = request.POST['remarks']
    mystatus = request.POST['status']
    mycase = request.POST['case']
    

    Hearing.objects.update_or_create(pk=id,defaults={'nextdate':mydate,'remarks':myremarks,'status':mystatus,'case_id':mycase})
    return redirect('/staff/all_hearing/')

def delete_hearing(request, pk):
    hearing = Hearing.objects.get(pk=pk)
    hearing.delete()
    return redirect('/staff/all_hearing/')

def logout_user(request):
    auth.logout(request)
    return redirect('/staff/login')


