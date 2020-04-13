from django.contrib import admin
from .models import User
from Vendor.models import Vendor
from Customer.models import Customer


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'vendor')


admin.site.register(User, UserAdmin)
admin.site.register(Vendor)
admin.site.register(Customer)