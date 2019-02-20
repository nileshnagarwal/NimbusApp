from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    """Base User Model + userType field"""
    
    USERTYPE_CHOICES = (
        (1, 'Developer'),
        (2, 'Admin'),
        (3, 'Sales'),
        (4, 'Traffic Incharge'),
        (5, 'Accounts'),
    )
    user_type = models.IntegerField(choices=USERTYPE_CHOICES, default=4)