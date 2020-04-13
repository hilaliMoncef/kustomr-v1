from django.contrib import messages
from Vendor.models import Vendor
from .models import Customer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import SignUpForm


class LandingPageView(View):
    """
    Cette page permet de récupérer les principales stats sur le commerçant
    """
    def get(self, request, *args, **kwargs):
        vendor = get_object_or_404(Vendor, pk=self.kwargs['vendor'])
        form = SignUpForm()
        return render(request, 'landing_page.html', locals())

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.add_message(request, messages.WARNING, 'Vous êtes déjà connecté.')
        else:
            vendor = get_object_or_404(Vendor, pk=self.kwargs['vendor'])
            form = SignUpForm(data=request.POST)
            if form.is_valid():
                user = form.save(commit=False)

                ## Adding the customer logic here
                user.is_customer = True
                user.is_vendor = False
                user.save()
                customer = Customer.objects.create(user=user, store_linked=vendor)
                
                ## Add the logic for confirmation here

                ## Then we log the newly created user
                login(request, user)
                messages.add_message(request, messages.SUCCESS, 'Votre compte a bien été créé. Veuillez le confirmer.')
                return redirect("customer_home")
            else:
                messages.add_message(request, messages.ERROR, 'Une ou plusieurs erreurs se sont produites durant la validation du formulaire.')
        return render(request, 'landing_page.html', locals())


class DashboardView(View):
    """
    Cette page permet de récupérer les principales stats sur le commerçant
    """
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html', locals())