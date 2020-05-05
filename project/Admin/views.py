from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from .forms import TrainingForm, VendorSignupForm
from Vendor.forms import VendorForm
from .models import Training, Message
from Vendor.models import Vendor, FacebookEvent, InstagramEvent
from Users.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.db.models import Avg, Count
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
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
        unread = Message.objects.filter(read=False).count()
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
        unread = Message.objects.filter(read=False).count()
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
            user.password = make_password(form.cleaned_data['password'])
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
                try:
                    send_mail(mail_subject, message, 'hilali.moncef@gmail.com', [to_email], html_message=message, fail_silently=False)
                except Exception as err:
                    print('Mailing error: {}'.format(err))
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
        unread = Message.objects.filter(read=False).count()
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



class SocialsView(LoginRequiredMixin, View):
    """
    Cette page permet de récupérer les formations en cours et en créer des nouvelles
    """
    http_method_names = ['get', 'post', 'put', 'delete']

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_staff:
            # Quick check if the user is admin
            return redirect('not-authorized')
        return super(SocialsView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        unread = Message.objects.filter(read=False).count()
        fb_events = FacebookEvent.objects.filter(processed=False)
        fb_events_done = FacebookEvent.objects.filter(processed=True).order_by('-date_processed')
        ig_events = InstagramEvent.objects.filter(processed=False)
        ig_events_done = InstagramEvent.objects.filter(processed=True).order_by('-date_processed')
        return render(request, 'admin/socials.html', locals())


def toggle_fb_processed(request, pk):
    event = get_object_or_404(FacebookEvent, pk=pk)
    if event.processed:
        event.processed = False
        event.date_processed = None
        event.save()
        messages.add_message(request, messages.SUCCESS, 'La publication de {} n\'est plus marquée comme traitée.'.format(event.vendor.store_name))
    else:
        event.processed = True
        event.date_processed = timezone.now()
        event.save()
        messages.add_message(request, messages.SUCCESS, 'La publication de {} a été traitée.'.format(event.vendor.store_name))
 
    return redirect('admin_socials')

def toggle_ig_processed(request, pk):
    event = get_object_or_404(InstagramEvent, pk=pk)
    if event.processed:
        event.processed = False
        event.date_processed = None
        event.save()
        messages.add_message(request, messages.SUCCESS, 'La publication de {} n\'est plus marquée comme traitée.'.format(event.vendor.store_name))
    else:
        event.processed = True
        event.date_processed = timezone.now()
        event.save()
        messages.add_message(request, messages.SUCCESS, 'La publication de {} a été traitée.'.format(event.vendor.store_name))
 
    return redirect('admin_socials')


class MessagesView(LoginRequiredMixin, View):
    """
    Cette page permet de récupérer les formations en cours et en créer des nouvelles
    """
    http_method_names = ['get', 'post', 'put', 'delete']

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_staff:
            # Quick check if the user is admin
            return redirect('not-authorized')
        return super(MessagesView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        messages_list = Message.objects.all()
        unread = Message.objects.filter(read=False).count()
        return render(request, 'admin/messages.html', locals())


def read_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    message.read = True
    message.save()
    return JsonResponse({}, status=201)

def delete_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    message.delete()
    return JsonResponse({}, status=201)