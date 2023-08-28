import django_filters
from django_filters import DateFilter, CharFilter
from .models import *

class PaymentFilter(django_filters.FilterSet):
    payment_date = DateFilter(field_name="date_paid", lookup_expr='gte')
    
    class Meta:
        model = Payment
        fields = '__all__'
        exclude = ['customer','date_paid','services']

class CustomerFilter(django_filters.FilterSet):
    name = CharFilter(field_name="name", lookup_expr='icontains')
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['full_name','loyalty_points','profile_pic','user']
