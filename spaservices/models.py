from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.models import Group

# Create your models here.
class SpaService(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    profile_pic = models.ImageField(default="user.png",null=True,blank=True)
    phone = models.IntegerField(null=True)
    loyalty_points = models.IntegerField(null=True, blank=True,default=0)

    def __str__(self):
        return str(self.user)
    
def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)

        Customer.objects.create(user=instance, name=instance.username) 
        print('Profile created')
post_save.connect(customer_profile, sender=User)
    
class Payment(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete= models.CASCADE)
    amount = models.FloatField(null=True)
    code = models.CharField(max_length=255, null=True)
    services = models.ManyToManyField(SpaService)
    date_paid = models.DateTimeField(auto_now_add=True,null=True)

    



   
    