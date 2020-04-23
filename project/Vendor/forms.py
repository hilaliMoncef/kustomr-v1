from django.forms import ModelForm
from django.forms import ValidationError
from .models import Vendor, RewardCardLayout, Discount, Offer, VendorOpeningHours


class VendorForm(ModelForm):
    class Meta:
        model = Vendor
        exclude = ['user']


class VendorOpeningHoursForm(ModelForm):
    class Meta:
        model = VendorOpeningHours
        exclude = ['vendor']


class RewardCardLayoutForm(ModelForm):
    class Meta:
        model = RewardCardLayout
        exclude = ['vendor']


class DiscountForm(ModelForm):
    class Meta:
        model = Discount
        exclude = ['vendor', 'is_active']
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if end_date < start_date:
            raise ValidationError("Les dates de début et de fin ne correspondent pas.")


class OfferForm(ModelForm):
    class Meta:
        model = Offer
        exclude = ['vendor', 'is_active']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if end_date < start_date:
            raise ValidationError("Les dates de début et de fin ne correspondent pas.")