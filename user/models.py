from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class user(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=15)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.email 
    