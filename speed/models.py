import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# class Constants:
 
    
class SpeedLimit(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    limit = models.IntegerField()

class UserInfo(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(default=datetime.date(1970, 1, 1))
    address = models.TextField(max_length=1000, default="")
    phone_no = models.BigIntegerField(null=True, default=9999999999)
    date_modified = models.DateTimeField('date_updated', blank=True, null=True)


class Vehicle(models.Model):
    register_no = models.CharField(max_length=100, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    desc = models.CharField(max_length=100)

class Penalty(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, unique=False, default="MP 20 AA 7106")
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False, default=1)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    speed = models.IntegerField()
    limit = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)