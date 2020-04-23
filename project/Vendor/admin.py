from django.contrib import admin
from .models import Vendor, RewardCardLayout, VendorOpeningHours, Discount, Offer


admin.site.register(Vendor)
admin.site.register(RewardCardLayout)
admin.site.register(Discount)
admin.site.register(Offer)
admin.site.register(VendorOpeningHours)
