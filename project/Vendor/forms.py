from django.forms import ModelForm
from django.forms import DateTimeField, DateTimeInput
from django.forms import ValidationError
from .models import Vendor, RewardCardLayout, Discount, Offer, VendorOpeningHours, InstagramEvent, FacebookEvent, Media, MailCampaign, SMSCampaign, Article
from django.utils import timezone


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


class DiscountImageForm(ModelForm):
    class Meta:
        model = Discount
        fields = ['image']


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


class OfferImageForm(ModelForm):
    class Meta:
        model = Offer
        fields = ['image']


class MediaForm(ModelForm):
    class Meta:
        model = Media
        fields = '__all__'


class InstagramEventForm(ModelForm):
    date_published = DateTimeField(
        input_formats = ['%Y-%m-%dT%H:%M'],
        widget = DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%Y-%m-%dT%H:%M')
    )

    class Meta:
        model = InstagramEvent
        exclude = ['vendor']

    def clean(self):
        cleaned_data = super().clean()
        date_published = cleaned_data.get("date_published")
        if date_published < timezone.now():
            raise ValidationError("Vous ne pouvez pas programmer des posts dans le passé.")


class FacebookEventForm(ModelForm):
    date_published = DateTimeField(
        input_formats = ['%Y-%m-%dT%H:%M'],
        widget = DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%Y-%m-%dT%H:%M')
    )

    class Meta:
        model = FacebookEvent
        exclude = ['vendor']

    def clean(self):
        cleaned_data = super().clean()
        date_published = cleaned_data.get("date_published")
        if date_published < timezone.now():
            raise ValidationError("Vous ne pouvez pas programmer des posts dans le passé.")


class MailCampaignForm(ModelForm):
    date_published = DateTimeField(
        input_formats = ['%Y/%m/%d %H:%M'],
        widget = DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%Y-%m-%dT%H:%M')
    )
    
    class Meta:
        model = MailCampaign
        exclude = ['vendor', 'date_processed']
    
    def clean(self):
        cleaned_data = super().clean()
        date_published = cleaned_data.get("date_published")
        if date_published < timezone.now():
            raise ValidationError("Vous ne pouvez pas programmer une campagne dans le passé.")


class SMSCampaignForm(ModelForm):
    date_published = DateTimeField(
        input_formats = ['%Y/%m/%d %H:%M'],
        widget = DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%Y-%m-%dT%H:%M')
    )
    
    class Meta:
        model = SMSCampaign
        exclude = ['vendor', 'date_processed']
    
    def clean(self):
        cleaned_data = super().clean()
        date_published = cleaned_data.get("date_published")
        if date_published < timezone.now():
            raise ValidationError("Vous ne pouvez pas programmer une campagne dans le passé.")


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        exclude = ['vendor', 'image']