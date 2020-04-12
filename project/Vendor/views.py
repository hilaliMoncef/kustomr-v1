from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
import qrcode


class DashboardView(LoginRequiredMixin, View):
    """
    Cette page permet de récupérer les principales stats sur le commerçant
    """
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard.html', locals())


class NewCustomerView(LoginRequiredMixin, View):
    """
    Cette page permet de générer un QR Code à scanner par l'utilisateur.
    Ce QR Code permet de rediriger l'utilisateur vers une Landing Page
    """
    def get(self, request, *args, **kwargs):
        link = "{}://{}{}".format(request.scheme, request.get_host(), reverse('customer_landing_page', args=(request.user.vendor.pk, slugify(request.user.vendor.store_name),)))
        return render(request, 'add_customer.html', locals())
