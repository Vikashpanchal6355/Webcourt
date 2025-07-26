from django.db import models
from django.contrib.auth.models import *


# Create your models here.
from django.db import models

from myadmin.models import Client

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'feedback'

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'contact'


class Appointment(models.Model):
    subject = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    client     = models.ForeignKey(Client,on_delete=models.CASCADE)
    
    # Client = models.ForeignKey('Client', on_delete=models.CASCADE)

    class Meta:
        db_table = 'appointment'