from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Vendor(models.Model):
    store_name = models.CharField(max_length=255)
    

class User(AbstractUser):
    is_vendor = models.BooleanField(default=False)
    vendor = models.OneToOneField(Vendor,on_delete=models.CASCADE, null=True, blank=True, related_name="user")