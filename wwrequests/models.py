from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Requests(models.Model):
    Type = models.CharField(max_length=20)
    Category = models.CharField(max_length=20)
    Request = models.CharField(max_length=500,unique=True)
    Remark = models.CharField(max_length=500,blank=True)
    From = models.ForeignKey(User,on_delete=models.CASCADE)
    Reference = models.CharField(max_length=50,blank=True)
    Schedule = models.CharField(max_length=50,blank=True)
    Status = models.CharField(max_length=20,blank=True)
    Comment = models.CharField(max_length=500,blank=True)
    pub_date = models.DateTimeField(auto_now=True)
    total_score = models.IntegerField(blank=True,default=0)

class Votes(models.Model):
    user = models.OneToOneField(User,
                                    on_delete=models.CASCADE,
                                    primary_key=True,)
    rank1=models.ManyToManyField(Requests,related_name='r1',blank=True)
    rank2=models.ManyToManyField(Requests,related_name='r2',blank=True)
    rank3=models.ManyToManyField(Requests,related_name='r3',blank=True)
    rank4=models.ManyToManyField(Requests,related_name='r4',blank=True)
    rank5=models.ManyToManyField(Requests,related_name='r5',blank=True)

class Discussion(models.Model):
    request = models.ForeignKey(Requests,on_delete=models.CASCADE)
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
