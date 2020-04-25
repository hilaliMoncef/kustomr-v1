from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse
from django.utils.text import slugify
from Admin.models import Training
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import VendorForm, RewardCardLayoutForm, OfferForm, DiscountForm, VendorOpeningHoursForm, OfferImageForm, DiscountImageForm
from .models import Discount, Offer
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
import qrcode
import json
import pandas as pd


class DashboardView(LoginRequiredMixin, View):
    """
    Cette page permet de récupérer les principales stats sur le commerçant
    """
    def get(self, request, *args, **kwargs):
        vendor = request.user.vendor
        customers = vendor.customers.all()[:5]

        customers_total = vendor.customers.count()
        
        # Creating a dataframe
        df = pd.DataFrame(vendor.customers.values('id', 'user__date_joined'))
        df['user__date_joined'] = pd.to_datetime(df['user__date_joined'])
        df.set_index('user__date_joined', drop=True, inplace=True)
        customer_count = list(df.resample('D').count()['id'])

        context = {
            'customers': customers,
            'customers_total': customers_total,
            'customer_count': customer_count
        }
        return render(request, 'vendor/home.html', context)


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
    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        if method == 'image':
            return self.update_image(*args, **kwargs)
        return super(DiscountsView, self).dispatch(*args, **kwargs)


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
            messages.add_message(request, messages.SUCCESS, 'La réduction "{}" a été créée.'.format(obj.name))
        else:
            errors = json.loads(form.errors.as_json())
            for error in errors:
                messages.add_message(request, messages.ERROR, '{} : {}'.format(error, errors[error][0]['message']))
        return redirect('vendor_discounts')

    def put(self, request, *args, **kwargs):
        form_type = request.POST['type']
        if form_type == 'discount':
            discount = get_object_or_404(Discount, pk=request.POST['pk'])
            form = DiscountForm(request.POST, instance=discount)
        else:
            offer = get_object_or_404(Offer, pk=request.POST['pk'])
            form = OfferForm(request.POST, instance=offer)
        
        if form.is_valid():
            instance = form.save()
            messages.add_message(request, messages.SUCCESS, 'La réduction "{}" a été modifiée.'.format(instance.name))
        else:
            errors = json.loads(form.errors.as_json())
            for error in errors:
                messages.add_message(request, messages.ERROR, '{} : {}'.format(error, errors[error][0]['message']))
        return redirect('vendor_discounts')

    def delete(self, request, *args, **kwargs):
        form_type = request.POST['type']
        if form_type == 'discount':
            obj = get_object_or_404(Discount, pk=request.POST['pk'])
        else:
            obj = get_object_or_404(Offer, pk=request.POST['pk'])
        messages.add_message(request, messages.SUCCESS, 'La formation "{}" a été supprimée.'.format(obj.name))
        obj.delete()
        return redirect('vendor_discounts')

    def update_image(self, request, *args, **kwargs):
        form_type = request.POST['type']
        if form_type == 'discount':
            discount = get_object_or_404(Discount, pk=request.POST['pk'])
            form = DiscountImageForm(request.POST, request.FILES, instance=discount)
        else:
            offer = get_object_or_404(Offer, pk=request.POST['pk'])
            form = OfferImageForm(request.POST, request.FILES, instance=offer)

        if form.is_valid():
            instance = form.save()
            messages.add_message(request, messages.SUCCESS, 'La réduction "{}" a été modifiée.'.format(instance.name))
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
        trainings = Training.objects.filter(is_active=True).order_by('-date_added')
        return render(request, 'vendor/training.html', locals())


class SettingsView(LoginRequiredMixin, View):
    """
    Cette vue permet de gérer les paramètres d'une page commerçant, 
    comme la carte de fidélité liée et les informations générales du compte.
    """
    def get(self, request, *args, **kwargs):
        vendor = request.user.vendor
        form_infos = VendorForm(instance=vendor)
        form_opening_hours = VendorOpeningHoursForm(instance=vendor.opening_hours)
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
        elif request.POST['form_type'] == 'opening_hours':
            form = VendorOpeningHoursForm(request.POST, instance=request.user.vendor.opening_hours)
            if form.is_valid() and form.has_changed():
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Vos horaires d\'ouverture ont été modifiées.')
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
