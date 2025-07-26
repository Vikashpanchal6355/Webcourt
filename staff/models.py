from django.db import models
from myadmin.models import *

# Create your models here.

class Hearing(models.Model):
	case     = models.ForeignKey(Case, on_delete=models.CASCADE)
	nextdate = models.DateField()
	remarks  = models.TextField()
	status   = models.CharField(max_length=30)
	

	class Meta:
		db_table='hearing'

# class Evidence(models.Model):
# 	case    = models.ForeignKey(Case, on_delete=models.CASCADE)
# 	title   = models.CharField(max_length=30)
# 	description   = models.TextField()
# 	evidence = models.CharField(max_length=255)
# 	class Meta:
# 		db_table = 'evidence'

# class Evidence(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     file = models.FileField(upload_to='evidence_files/')
#     created_at = models.DateTimeField(auto_now_add=True)
	
# class Meta:
# 		db_table='evidence'


class Evidence(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    file = models.FileField(upload_to='evidence_files/')
    upload_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'evidence'
