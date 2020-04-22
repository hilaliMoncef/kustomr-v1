from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import VendorForm, RewardCardLayoutForm, OfferForm, DiscountForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
import qrcode
import json


class DashboardView(LoginRequiredMixin, View):
    """
    Cette page permet de récupérer les principales stats sur le commerçant
    """
    def get(self, request, *args, **kwargs):
        customers = request.user.vendor.customers.all()[:5]
        return render(request, 'vendor/home.html', locals())


class CustomersView(LoginRequiredMixin, View):
    """
    Cette page permet de gérer au commerçant de gérer ses clients
    """
    def get(self, request, *args, **kwargs):
        customers = request.user.vendor.customers.all()
        return render(request, 'vendor/all_customers.html', locals())


class DiscountsView(LoginRequiredMixin, View):
    """
    Cette page permet de récupérer les principales stats sur le commerçant
    """
    def get(self, request, *args, **kwargs):
        discount_form = DiscountForm()
        offer_form = OfferForm()
        vendor = request.user.vendor
        future_reductions = vendor.discounts.filter(start_date__gt=timezone.now()).count() + vendor.offers.filter(start_date__gt=timezone.now()).count()
        active_reductions = vendor.discounts.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now()).count() + vendor.offers.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now()).count()
        expired_reductions = vendor.discounts.filter(end_date__lt=timezone.now()).count() + vendor.offers.filter(end_date__lt=timezone.now()).count()
        return render(request, 'vendor/discounts.html', locals())

    def post(self, request, *args, **kwargs):
        form_type = request.POST['type']
        if form_type == 'discount':
            form = DiscountForm(request.POST, request.FILES)
        else:
            form = OfferForm(request.POST, request.FILES)
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.vendor = request.user.vendor
            obj.save()
        else:
            errors = json.loads(form.errors.as_json())
            for error in errors:
                messages.add_message(request, messages.ERROR, '{} : {}'.format(error, errors[error][0]['message']))
        return redirect('vendor_discounts')


class MarketingView(LoginRequiredMixin, View):
    """
    Cette page permet de récupérer les principales stats sur le commerçant
    """
    def get(self, request, *args, **kwargs):
        customers = request.user.vendor.customers.all()[:5]
        return render(request, 'vendor/marketing.html', locals())


class SocialView(LoginRequiredMixin, View):
    """
    Cette page permet de récupérer les principales stats sur le commerçant
    """
    def get(self, request, *args, **kwargs):
        customers = request.user.vendor.customers.all()[:5]
        return render(request, 'vendor/social.html', locals())


class TrainingView(LoginRequiredMixin, View):
    """
    Cette page permet de récupérer les principales stats sur le commerçant
    """
    def get(self, request, *args, **kwargs):
        customers = request.user.vendor.customers.all()[:5]
        return render(request, 'vendor/training.html', locals())


class SettingsView(LoginRequiredMixin, View):
    """
    Cette vue permet de gérer les paramètres d'une page commerçant, 
    comme la carte de fidélité liée et les informations générales du compte.
    """
    def get(self, request, *args, **kwargs):
        vendor = request.user.vendor
        form_infos = VendorForm(instance=vendor)
        form_reward_card = RewardCardLayoutForm(instance=vendor.reward_card_layout)
        form_password_change = PasswordChangeForm(request.user)
        return render(request, 'vendor/settings.html', locals())

    def post(self, request, *args, **kwargs):
        if request.POST['form_type'] == 'infos':
            # If the Information form is submitted
            form = VendorForm(request.POST, instance=request.user.vendor)
            if form.is_valid() and form.has_changed():
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Vos informations personnelles ont été modifiées.')
            return redirect('vendor_settings')
        elif request.POST['form_type'] == 'reward_card':
            # If the RewardCardLayout form is submitted
            form = RewardCardLayoutForm(request.POST, request.FILES, instance=request.user.vendor.reward_card_layout)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Le design a bien été modifié.')
            else:
                errors = json.loads(form.errors.as_json())
                for error in errors:
                    messages.add_message(request, messages.ERROR, errors[error][0]['message'])
        elif request.POST['form_type'] == 'password':
            # If the PasswordChange form is submitted -- we use the default form from Django
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                # Updating the password logs out all other sessions for the user
                # except the current one.
                update_session_auth_hash(request, form.user)
                messages.add_message(request, messages.SUCCESS, 'Votre mot de passé a été modifié.')
            else:
                errors = json.loads(form.errors.as_json())
                for error in errors:
                    messages.add_message(request, messages.ERROR, errors[error][0]['message'])
        else:
            # In case we have a weird user manipulation
            messages.add_message(request, messages.ERROR, 'Erreur inconnue')

        # Always redirect to the settings page
        return redirect('vendor_settings')

# A adapter, uniquement les admins qui générent des nouveaux clients
class NewCustomerView(LoginRequiredMixin, View):
    """
    Cette page permet de générer un QR Code à scanner par l'utilisateur.
    Ce QR Code permet de rediriger l'utilisateur vers une Landing Page
    """
    def get(self, request, *args, **kwargs):
        link = "{}://{}{}".format(request.scheme, request.get_host(), reverse('customer_landing_page', args=(request.user.vendor.pk, slugify(request.user.vendor.store_name),)))
        return render(request, 'add_customer.html', locals())
