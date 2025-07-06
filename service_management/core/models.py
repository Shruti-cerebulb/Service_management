from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)
    contact = models.CharField(max_length=15, blank=True, null=True)


    def str(self):
        return self.user.username
    
class ServiceCategory(models.Model):
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category_name
    
class Service(models.Model):
    service_category = models.ForeignKey(ServiceCategory,on_delete=models.CASCADE,related_name='services')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    duration = models.PositiveIntegerField()
    
    def __str__(self):
         return self.name

