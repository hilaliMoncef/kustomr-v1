from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from .forms import TrainingForm, VendorSignupForm
from Vendor.forms import VendorForm
from .models import Training
from Vendor.models import Vendor
from Users.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.db.models import Avg, Count
import json


class DashboardView(LoginRequiredMixin, View):
    """
    Cette page permet de récupérer les principales stats pour le panel admin
    """
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_staff:
            # Quick check if the user is admin
            return redirect('not-authorized')
        return super(DashboardView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'admin/home.html', locals())


class VendorsView(LoginRequiredMixin, View):
    """
    Cette page permet de récupérer les principales stats pour le panel admin
    """
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_staff:
            # Quick check if the user is admin
            return redirect('not-authorized')
        return super(VendorsView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        vendors = Vendor.objects.all()
        vendors_count = vendors.count()
        nb_clients_avg = Vendor.objects.all().annotate(nb_customers=Count('customers')).aggregate(Avg('nb_customers'))['nb_customers__avg']
        password = User.objects.make_random_password()
        form = VendorForm()
        return render(request, 'admin/vendors.html', locals())

    def post(self, request, *args, **kwargs):
        form = VendorSignupForm(request.POST)
        if form.is_valid():
            # The User form is OK
            user = form.save(commit=False)
            user.is_vendor = True
            user.is_customer = False
            user.save()
            form_vendor = VendorForm(request.POST)
            if form_vendor.is_valid():
                # The Vendor form is OK
                vendor = form_vendor.save(commit=False)
                vendor.user = user
                vendor.save()

                ## Sending a confirmation mail
                current_site = get_current_site(request)
                mail_subject = 'Votre dashboard Elevator'
                message = render_to_string('emails/vendor_created.html', {
                    'domain': current_site.domain,
                    'vendor': vendor,
                    'password': request.POST['password']
                })
                to_email = user.email
                send_mail(mail_subject, message, 'hilali.moncef@gmail.com', [to_email], html_message=message, fail_silently=False)

                messages.add_message(request, messages.SUCCESS, 'Le commerçant a été ajouté. Un email récapitulatif a été envoyé.')
            else:
                errors = json.loads(form_vendor.errors.as_json())
                for error in errors:
                    messages.add_message(request, messages.ERROR, '{} : {}'.format(error, errors[error][0]['message']))
        else:
            errors = json.loads(form.errors.as_json())
            for error in errors:
                messages.add_message(request, messages.ERROR, '{} : {}'.format(error, errors[error][0]['message']))
        return redirect('admin_vendors')


class TrainingsView(LoginRequiredMixin, View):
    """
    Cette page permet de récupérer les formations en cours et en créer des nouvelles
    """
    http_method_names = ['get', 'post', 'put', 'delete']

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_staff:
            # Quick check if the user is admin
            return redirect('not-authorized')

        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(TrainingsView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = TrainingForm()
        trainings = Training.objects.all()
        frees = Training.objects.filter(is_free=True).count()
        premiums = Training.objects.filter(is_free=False).count()
        return render(request, 'admin/trainings.html', locals())

    def post(self, request, *args, **kwargs):
        form = TrainingForm(request.POST)
        if form.is_valid():
            formation = form.save()
            messages.add_message(request, messages.SUCCESS, 'La formation "{}" a été créée.'.format(formation.name))
        return redirect('admin_trainings')

    def put(self, request, *args, **kwargs):
        training = get_object_or_404(Training, pk=request.POST['pk'])
        form = TrainingForm(request.POST, instance=training)
        if form.is_valid():
            formation = form.save()
            messages.add_message(request, messages.SUCCESS, 'La formation "{}" a été modifiée.'.format(formation.name))
        return redirect('admin_trainings')

    def delete(self, request, *args, **kwargs):
        training = get_object_or_404(Training, pk=request.POST['pk'])
        messages.add_message(request, messages.SUCCESS, 'La formation "{}" a été supprimée.'.format(training.name))
        training.delete()
        return redirect('admin_trainings')
