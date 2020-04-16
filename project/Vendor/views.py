from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import VendorForm, RewardCardLayoutForm
import qrcode


class DashboardView(LoginRequiredMixin, View):
    """
    Cette page permet de récupérer les principales stats sur le commerçant
    """
    def get(self, request, *args, **kwargs):
        customers = request.user.vendor.customers.all()
        return render(request, 'vendor/home.html', locals())




class SettingsView(LoginRequiredMixin, View):
    """
    Cette vue permet de gérer les paramètres d'une page commerçant, 
    comme la carte de fidélité liée et les informations générales du compte.
    """
    def get(self, request, *args, **kwargs):
        vendor = request.user.vendor
        form_infos = VendorForm(instance=vendor)
        form_reward_card = RewardCardLayoutForm(instance=vendor.reward_card_layout)
        return render(request, 'vendor/settings.html', locals())

    def post(self, request, *args, **kwargs):
        if request.POST['form_type'] == 'infos':
            # If the Information form is submitted
            form = VendorForm(request.POST, instance=request.user.vendor)
            if form.is_valid() and form.has_changed():
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Vos informations personnelles ont été modifiées')
            return redirect('vendor_settings')
        elif request.POST['form_type'] == 'reward_card':
            # If the RewardCardLayout form is submitted
            form = RewardCardLayoutForm(request.POST, request.FILES, instance=request.user.vendor.reward_card_layout)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Le design a bien été modifié')
            else:
                print(form.errors)
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
