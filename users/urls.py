from django.urls import path
from . import views

urlpatterns = [
    path('mainMessage', views.mainMessage, name='mainMessage'),
    path('mainUser', views.mainUser, name='mainUser'),
    path('mainAppointment', views.mainAppointment, name='mainAppointment'),
    path('mainLogin', views.mainLogin, name='mainLogin'),
    path('mainDashboard', views.mainDashboard, name='mainDashboard'),
    path('<int:user_id>/removeUser/', views.removeUser, name='removeUser'),
    path('acceptUser/<int:user_id>/', views.acceptUser, name='acceptUser'),
    path('declineUser/<int:user_id>/', views.declineUser, name='declineUser'),
    path('rejectRequest/<int:sched_id>/', views.rejectRequest, name='rejectRequest'),
    path('approveRequest/<int:sched_id>/', views.approveRequest, name='approveRequest'),
    path('<int:message_id>/removeMessage/', views.removeMessage, name='removeMessage'),
    
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('homepage', views.homepage, name='homepage'),
    path('register', views.register, name='register'),
    
    path('doctorAppointment', views.doctorAppointment, name='doctorAppointment'),
    path('doctorDashboard', views.doctorDashboard, name='doctorDashboard'),
    path('doctorPatients', views.doctorPatients, name='doctorPatients'),
    
    path('dentistPatients', views.dentistPatients, name='dentistPatients'),
    path('dentistAppointment', views.dentistAppointment, name='dentistAppointment'),
    path('dentistDashboard', views.dentistDashboard, name='dentistDashboard'),
    
    path('nursePatientList', views.nursePatientList, name='nursePatientList'),
    path('nurseDashboard', views.nurseDashboard, name='nurseDashboard'),
    
    path('residentDashboard', views.residentDashboard, name='residentDashboard'),
    
    path('logoutUser', views.logoutUser, name='logoutUser'),
]