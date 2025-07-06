from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)
    contact = models.CharField(max_length=15, blank=True, null=True)


    def _str_(self):
        return self.user.username
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Services(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField()

    def __str__(self):
        return self.name
