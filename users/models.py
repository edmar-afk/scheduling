from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Appointment(models.Model):
    name = models.CharField(max_length=250)
    note = models.CharField(max_length=10000)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.DateField()
    status = models.CharField(max_length=250)
    
    
class Event(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    age = models.CharField(max_length=200)
    gender = models.TextField()
    date = models.DateTimeField()
    barangay = models.TextField()
    phone_num = models.TextField()
    status = models.CharField(max_length=250)
  
    def __str__(self):
        return self.name
    
class Message(models.Model):
    sender = models.TextField()
    message = models.TextField()