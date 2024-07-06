from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth import authenticate, login
from django.db.models import Q
from .models import Event, Message
from datetime import datetime
# Create your views here.


def mainMessage(request):
    feeback = Message.objects.all().order_by('-id')
    
    context = {
        'feeback': feeback
    }
    
    return render(request, 'main/messages.html', context)

def mainLogin(request):
    return render(request, 'main/mainLogin.html')


def mainUser(request):
    users = User.objects.all().order_by('-id')
    
    context = {
        'users': users,
    }
    return render(request, 'main/users.html', context)


def mainDashboard(request):
    users = User.objects.all().order_by('-id')
    
    context = {
        'users': users
    }
    
    return render(request, 'main/index.html', context)

def mainAppointment(request):
    schedule = Event.objects.filter(status='Approved').order_by('-id')
    
    context = {
        'schedule': schedule,
    }
    return render(request, 'main/checkAppointment.html', context)

def homepage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        info = authenticate(username=username, password=password)
        if info is not None:
            login(request, info)
            if info.is_staff and info.last_name == 'Doctor':
                return redirect('doctorDashboard')
            elif info.is_staff and info.last_name == 'Dentist':
                return redirect('dentistDashboard')
            elif info.is_staff and info.last_name == 'Nurse':
                return redirect('nurseDashboard')
            elif info.is_staff and info.last_name == 'Resident':
                return redirect('residentDashboard')
            else:
                messages.error(request, "You are not approve to the admin. Please wait")
                return redirect('homepage')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('homepage')
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        fullname = request.POST['fullname']
        role = request.POST['role']
        address = request.POST['address']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'School Id already taken.')
                return redirect('register')

            else:
                new_student = User.objects.create_user(
                    first_name=fullname, username=username, password=password1, last_name=role, email=address, is_staff=False, is_superuser=False )
                new_student.save()
                messages.success(request, 'Account created')
                return redirect('homepage')
        else:
            messages.error(request, 'Password does not match.')
            return redirect('register')
    return render(request, 'register.html')



def doctorAppointment(request):
    schedule = Event.objects.filter(
    (Q(doctor__last_name='Doctor') | Q(doctor=request.user)) & Q(status='Approved')
).order_by('-id')
    
    context = {
        'schedule': schedule,
    }
    return render(request, 'doctor/checkAppointment.html', context)

def doctorDashboard(request):
    schedule = Event.objects.filter(Q(doctor__last_name='Doctor') | Q(doctor=request.user)).order_by('-id')
    
    context = {
        'schedule': schedule,
    }
    return render(request, 'doctor/index.html', context)

def doctorPatients(request):
    schedule = Event.objects.filter(
    (Q(doctor__last_name='Doctor') | Q(doctor=request.user)) & Q(status='Approved')
).order_by('-id')
    
    context = {
        'schedule': schedule,
    }
    return render(request, 'doctor/patientList.html', context)


def residentDashboard(request):
    workers = User.objects.filter(Q(last_name='Doctor') | Q(last_name='Dentist'))
    events = Event.objects.all()
    if request.method == 'POST':
        date_str = request.POST['date']
        doctor_id = request.POST['doctor']
        fullname = request.POST['fullname']
        age = request.POST['age']
        gender = request.POST['gender']
        barangay = request.POST['barangay']
        phone_num = request.POST['phone_num']

        # Parse the date string to a datetime object
        date = datetime.strptime(date_str, '%m/%d/%Y')

        # Fetch the User instance for the doctor
        doctor = User.objects.get(pk=doctor_id)
       
        new_schedule = Event.objects.create(status='Pending',doctor=doctor, date=date,age=age, name=fullname, gender=gender, barangay=barangay, phone_num=phone_num)
        new_schedule.save()
        messages.success(request, 'Schedule Requested')
        return redirect(request.META.get('HTTP_REFERER'))

    context = {
        'workers': workers,
        'events': events
    }
    return render(request, 'resident/index.html', context)



def nursePatientList(request):
    patients = Event.objects.filter(status='Approved').order_by('-id')
    
    context = {
        'patients': patients
    }
    
    return render(request, 'nurse/patientList.html', context)

def nurseDashboard(request):
    clearance = Event.objects.all().order_by('-id')
    
    context = {
        'clearance': clearance
    }
    
    return render(request, 'nurse/index.html', context)



def dentistPatients(request):
    schedule = Event.objects.filter(
    (Q(doctor__last_name='Dentist') | Q(doctor=request.user)) & Q(status='Approved')
).order_by('-id')
    
    context = {
        'schedule': schedule,
    }
    return render(request, 'dentist/patientList.html', context)

def dentistAppointment(request):
    schedule = Event.objects.filter(
    (Q(doctor__last_name='Dentist') | Q(doctor=request.user)) & Q(status='Approved')
).order_by('-id')
    
    context = {
        'schedule': schedule,
    }
    return render(request, 'dentist/checkAppointment.html', context)

def dentistDashboard(request):
    schedule = Event.objects.filter(Q(doctor__last_name='Dentist') | Q(doctor=request.user)).order_by('-id')
    
    context = {
        'schedule': schedule,
    }
    return render(request, 'doctor/index.html', context)

def removeMessage(request, message_id):
    Message.objects.filter(id=message_id).delete()
    messages.success(request, 'Message Removed')
    return redirect(request.META.get('HTTP_REFERER'))

def removeUser(request, user_id):
    User.objects.filter(id=user_id).delete()
    messages.success(request, 'User Removed')
    return redirect(request.META.get('HTTP_REFERER'))


def acceptUser(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_staff = True
    user.save()
    # You can redirect to a success page or to the same page
    messages.success(request, 'User Accepted')
    return redirect(request.META.get('HTTP_REFERER'))

def declineUser(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_staff = False
    user.save()
    # You can redirect to a success page or to the same page
    messages.success(request, 'User Declined')
    return redirect(request.META.get('HTTP_REFERER'))

def logoutUser(request):
    auth.logout(request)
    messages.success(request, "Logged out Successfully!")
    return redirect('homepage')





def rejectRequest(request, sched_id):
    event = Event.objects.get(pk=sched_id)
    event.status = 'Rejected'
    event.save()
    # You can redirect to a success page or to the same page
    messages.success(request, 'Request Rejected!')
    return redirect(request.META.get('HTTP_REFERER'))

def approveRequest(request, sched_id):
    event = Event.objects.get(pk=sched_id)
    event.status = 'Approved'
    event.save()
    # You can redirect to a success page or to the same page
    messages.success(request, 'Request Approved!')
    return redirect(request.META.get('HTTP_REFERER'))


def about(request):
    return render(request, 'about.html')

def contact(request):
    
    if request.method == 'POST':
        name = request.POST['fname']
        message = request.POST['message']
        
        new_message = Message.objects.create(sender=name, message=message)
        new_message.save()
        messages.success(request, 'Message Sent!')
    
    return render(request, 'contact.html')