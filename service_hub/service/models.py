from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    contact = models.CharField(max_length=12,blank=True,null=True)
    address = models.TextField(blank=True,null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'contact', 'address'] 

    def __str__(self):
        return self.username


