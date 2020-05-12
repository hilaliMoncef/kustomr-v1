from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from Vendor.models import Vendor
from .models import Customer, CustomerToken
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .forms import SignUpForm
from django.utils.text import slugify
from django.utils import timezone


class LandingPageView(View):
    """
    Cette page permet de récupérer les principales stats sur le commerçant
    """
    def get(self, request, *args, **kwargs):
        vendor = get_object_or_404(Vendor, pk=self.kwargs['vendor'])
        if request.user.is_authenticated:
            if request.user.is_customer:
                return redirect("customer_home", vendor=vendor.pk, store_name=slugify(vendor.store_name), token=request.user.get_customer(store=vendor.pk).token.token)
            return redirect('home')
        form = SignUpForm()
        return render(request, 'customer/landing_page.html', locals())

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
                current_site = get_current_site(request)
                mail_subject = 'Bienvenue chez {} !'.format(vendor.store_name)
                message = render_to_string('emails/register_confirmation.html', {
                    'customer': customer,
                    'domain': current_site.domain,
                    'vendor': vendor
                })
                to_email = user.email
                send_mail(mail_subject, message, 'no-reply@app.kustomr.fr', [to_email], html_message=message, fail_silently=False)

                ## Then we log the newly created user
                login(request, user)
                messages.add_message(request, messages.SUCCESS, 'Votre compte a bien été créé.')
                return redirect("customer_home", vendor=vendor.pk, store_name=slugify(vendor.store_name), token=customer.token.token)
            else:
                messages.add_message(request, messages.ERROR, 'Une ou plusieurs erreurs se sont produites durant la validation du formulaire.')
        return render(request, 'customer/landing_page.html', locals())


class DashboardView(View):
    """
    Cette page permet d'afficher a tout detenteur du bon token son tableau de bord pour ce commerçant
    """
    def get(self, request,  *args, **kwargs):
        vendor = get_object_or_404(Vendor, pk=self.kwargs['vendor'])
        token = get_object_or_404(CustomerToken, token=self.kwargs['token'])
        if not request.user.is_authenticated:
            login(request, token.customer.user)
        customer = request.user.get_customer(store=self.kwargs['vendor'])
        discounts = list(vendor.discounts.filter(is_active=True, end_date__gte=timezone.now()))
        offers = list(vendor.offers.filter(is_active=True, end_date__gte=timezone.now()))
        articles = vendor.articles.all()
        
        context = {
            'vendor': vendor,
            'customer': customer,
            'discounts': discounts + offers,
            'articles': articles
        }
        return render(request, 'customer/home.html', context)