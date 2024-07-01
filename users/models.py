from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Appointment(models.Model):
    name = models.CharField(max_length=250)
    note = models.CharField(max_length=10000)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.DateField()
    status = models.CharField(max_length=250)