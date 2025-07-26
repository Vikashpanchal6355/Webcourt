from django.contrib.auth.models import User
from django.db import models
from datetime import date
from django.utils import timezone

# Create your models here.

class Staff(models.Model):
    user    = models.OneToOneField(User,on_delete=models.CASCADE)
    gender   = models.CharField(max_length=30)
    dob      = models.DateField(default=timezone.now)
    education = models.CharField(max_length=50)
    phone  = models.BigIntegerField()
    address  = models.CharField(max_length=80)
    # date     = models.DateField(default=date.today())
    date     = models.DateField(default=timezone.now)

    class Meta:
        db_table = 'staff'

class Client(models.Model):
    user    = models.OneToOneField(User,on_delete=models.CASCADE)
    middle_name=models.CharField(max_length=30)
    gender   = models.CharField(max_length=30) 
    contact  = models.BigIntegerField()
    address  = models.CharField(max_length=80)
    date     = models.DateField(default=timezone.now)
    # date     = models.DateField(default=date.today())

    class Meta:
        db_table = 'client'

class Case(models.Model):
    case_title = models.CharField(max_length=30)
    description = models.TextField()
    fir_date = models.DateField()
    fir_station = models.CharField(max_length=30)
    crimetype = models.CharField(max_length=30)
    fir_copy = models.FileField(blank=True, null=True)
    status  = models.CharField(max_length=30,default='running')
    client   = models.ForeignKey(Client, on_delete=models.CASCADE)
    staff    = models.ForeignKey(Staff, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'case'


# class Evidence(models.Model):
#     case = models.ForeignKey(Case, on_delete=models.CASCADE)
#     evidence_title = models.CharField(max_length=30)
#     evidence_description = models.TextField()
#     evidence_file = models.FileField(blank=True, null=True)
#     date = models.DateField(default=timezone.now)

#     class Meta:
#         db_table = 'evidence'