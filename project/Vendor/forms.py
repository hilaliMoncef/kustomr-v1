from django.forms import ModelForm
from .models import Vendor, RewardCardLayout


class VendorForm(ModelForm):
    class Meta:
        model = Vendor
        exclude = ['user']


class RewardCardLayoutForm(ModelForm):
    class Meta:
        model = RewardCardLayout
        exclude = ['vendor']