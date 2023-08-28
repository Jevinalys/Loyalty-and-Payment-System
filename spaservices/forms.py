from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Payment, Customer, SpaService

class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = ['customer','amount','code','services']
  
 #       labels = {
           # 'customer':'',
           # 'amount':'',
            #'services':''
    #    }

  #      widgets = {
           # 'customer':forms.TextInput(attrs={'class':'fo rm-control','placeholder': 'Your name'}),
            #'amount':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Amount'}),
            #'services':forms.TextInput(attrs={'class':'form-select', 'placeholder': 'Select service'})
   #     }
class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone','profile_pic']

class PointsForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['loyalty_points']

class UserForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['profile_pic']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
