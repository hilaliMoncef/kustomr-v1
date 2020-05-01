from django.contrib import admin
from .models import Customer, CustomerToken, CustomersList


admin.site.register(Customer)
admin.site.register(CustomerToken)
admin.site.register(CustomersList)