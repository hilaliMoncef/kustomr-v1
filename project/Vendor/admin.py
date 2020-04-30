from django.contrib import admin
from .models import Vendor, RewardCardLayout, VendorOpeningHours, Discount, Offer, InstagramEvent, FacebookEvent


admin.site.register(Vendor)
admin.site.register(RewardCardLayout)
admin.site.register(Discount)
admin.site.register(Offer)
admin.site.register(VendorOpeningHours)
admin.site.register(InstagramEvent)
admin.site.register(FacebookEvent)
