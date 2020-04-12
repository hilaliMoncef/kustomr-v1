from django.contrib import admin
from .models import User, Vendor


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'vendor')


admin.site.register(User, UserAdmin)
admin.site.register(Vendor)