from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import PaymentForm, CustomerForm, CreateUserForm, PointsForm
from .models import *
from .filters import PaymentFilter, CustomerFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request,'Account was created for ' + username)
            return redirect('login')

    context = {'form':form}
    return render (request, 'spaservices/register.html', context)

@unauthenticated_user
def loginPage(request):
        
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request,username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render (request, 'spaservices/login.html', context)

def logoutUser(request):
            logout(request)
            return redirect('login')

def ladybirdhome(request):

    return render (request, 'spaservices/base.html')


@login_required(login_url='login')
@admin_only
def home(request):
    payments = Payment.objects.all()
    home_customers = Customer.objects.all()
    daily_sales = Payment.objects.count()
    monthly_sales = Payment.objects.count()
    
    customer_filter = CustomerFilter(request.GET, queryset=home_customers)
    home_customers = customer_filter.qs



    context = {'payments':payments, 'home_customers':home_customers, 'daily_sales':daily_sales, 'monthly_sales':monthly_sales, 'customer_filter':customer_filter}

    return render(request, 'spaservices/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    payments = request.user.customer.payment_set.all()
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()

    context = {'payments':payments, 'customer':customer,'form':form}
    return render(request, 'spaservices/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customers(request, pk):
    customers = Customer.objects.get(id=pk)
    payments = customers.payment_set.all()

    context = {'customers':customers,'payments':payments}
    return render(request, 'spaservices/customers.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customerlist(request):
    customerl = Customer.objects.all()
    customer_count = customerl.count()
   
    customer_filter = CustomerFilter(request.GET, queryset=customerl)
    customerl = customer_filter.qs

    context = {'customerl':customerl, 'customercount': customer_count, 'customer_filter':customer_filter }

    return render(request, 'spaservices/customer_list.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def services(request):
    return render(request, 'spaservices/services.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def payment(request):
    payment = Payment.objects.all()

    payFilter = PaymentFilter(request.GET, queryset=payment)
    payment = payFilter.qs
     
    context = {'payment':payment, 'payFilter':payFilter}
    
    return render(request, 'spaservices/payments.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createPayment(request, pk):
    customers = Customer.objects.get(id=pk)
    form = PaymentForm(initial = {'customer':customers})
    if request.method == 'POST':
        form = PaymentForm(request.POST) 
        if form.is_valid():
            new_amount = form.cleaned_data['amount']
            new_points = new_amount*0.1  
            instance=form.save(commit=False)
            points = instance.customer.loyalty_points
            i = points + new_points
            customers.loyalty_points= i
            customers.save()
            form.save()

            return redirect('/home')

    context = {'form':form,}

    return render(request, 'spaservices/payment_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def redeemPoints(request, pk):
    customers = Customer.objects.get(id=pk)
    form = PointsForm(initial = {'loyalty_points':customers.loyalty_points})
    if request.method == 'POST':
        form = PointsForm(request.POST) 
        if form.is_valid():
            current_points = customers.loyalty_points
            redeem_points = form.cleaned_data['loyalty_points']
            customers.loyalty_points=current_points-redeem_points
            
            customers.save()
            #form.save()

            return redirect('/home')

    context = {'form':form,}

    return render(request, 'spaservices/points.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updatePayment(request, pk):

    payment = Payment.objects.get(id=pk)
    form = PaymentForm(instance=payment)

    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect('/home')
        
    context = {'form':form}
    return render(request, 'spaservices/payment_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/home')
        
    context = {'form':form}
    return render(request, 'spaservices/customer_update.html',context)

@csrf_exempt
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createCustomer(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/home')

    context = {'form':form}

    return render(request, 'spaservices/customer_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])  
def deleteItem(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == "POST":
        customer.delete()
        return redirect('/home')

    context = {'item':customer}
    return render(request, 'spaservices/delete.html',context)

             
                   