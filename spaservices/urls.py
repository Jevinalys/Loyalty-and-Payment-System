from . import views
from django.urls import path


urlpatterns = [
    path('', views.ladybirdhome, name="ladybird"),
    path('home/', views.home, name="home"),
    path('customers/<str:pk>/', views.customers, name="customers"),
    path('services/', views.services, name="services"),
    path('payment/', views.payment, name="payment"), 
    path('customerlist/', views.customerlist, name="custlist"),
    path('payment_form/<str:pk>/', views.createPayment, name="payment_form"),
    path('points/<str:pk>/', views.redeemPoints, name="points"),
    path('update_form/<str:pk>/', views.updatePayment, name="updatePayment"),
    path('update_customer/<str:pk>/', views.updateCustomer, name="updateCustomer"),
    path('delete/<str:pk>/', views.deleteItem, name="delete"),
    path('customer_form/', views.createCustomer, name="customer_form"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('user/', views.userPage, name="userpage"),

]