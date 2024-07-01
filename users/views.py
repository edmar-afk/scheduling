from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth import authenticate, login
# Create your views here.

def mainLogin(request):
    return render(request, 'main/mainLogin.html')

def mainDashboard(request):
    users = User.objects.all().order_by('-id')
    
    context = {
        'users': users
    }
    
    return render(request, 'main/index.html', context)


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



def doctorDashboard(request):
    return render(request, 'doctor/index.html')




def residentDashboard(request):
    return render(request, 'resident/index.html')




def nurseDashboard(request):
    return render(request, 'nurse/index.html')




def dentistDashboard(request):
    return render(request, 'dentist/index.html')



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