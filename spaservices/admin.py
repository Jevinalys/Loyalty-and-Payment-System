from django.contrib import admin
from .models import *


# Register your models here.

#class SpaServiceAdmin(admin.ModelAdmin):
    #list_display = ('services',)

#class CustomerAdmin(admin.ModelAdmin):
   # list_display = ('name', 'phone')

admin.site.register(SpaService)
admin.site.register(Customer)
admin.site.register(Payment)