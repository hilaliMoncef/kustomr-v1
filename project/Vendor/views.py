from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.views import View
from django.urls import reverse
from django.utils.text import slugify
from Admin.models import Training, Message
from Admin.forms import MessageForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import VendorForm, RewardCardLayoutForm, OfferForm, DiscountForm, VendorOpeningHoursForm, OfferImageForm, DiscountImageForm, InstagramEventForm, FacebookEventForm, MediaForm, MailCampaignForm, SMSCampaignForm, ArticleForm
from .models import Discount, Offer, FacebookEvent, InstagramEvent, MailCampaign, SMSCampaign, Article
from Customer.models import Customer, CustomersList, Transaction
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from django.db.models import Avg, Count, Sum, Q
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.core.mail import send_mail, get_connection, EmailMultiAlternatives
from django.forms.models import model_to_dict
import datetime
import qrcode
import json
import pandas as pd



def send_mass_html_mail(datatuple, fail_silently=False, user=None, password=None, 
                        connection=None):
    """
    Given a datatuple of (subject, text_content, html_content, from_email,
    recipient_list), sends each message to each recipient list. Returns the
    number of emails sent.

    If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
    If auth_user and auth_password are set, they're used to log in.
    If auth_user is None, the EMAIL_HOST_USER setting is used.
    If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.

    """
    connection = connection or get_connection(
        username=user, password=password, fail_silently=fail_silently)
    messages = []
    for subject, text, html, from_email, recipient in datatuple:
        message = EmailMultiAlternatives(subject, text, from_email, recipient)
        message.attach_alternative(html, 'text/html')
        messages.append(message)
    return connection.send_messages(messages)


class DashboardView(LoginRequiredMixin, View):
    """
    Cette page permet de récupérer les principales stats sur le commerçant
    """
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_vendor:
            # Quick check if the user is vendor
            return redirect('not-authorized')
        return super(DashboardView, self).dispatch(*args, **kwargs)
        
    def get(self, request, *args, **kwargs):
        vendor = request.user.vendor
        customers = vendor.customers.all()[:5]

        customers_total = vendor.customers.count()
        
        # Creating a dataframe
        if customers_total > 0:
            df = pd.DataFrame(vendor.customers.values('id', 'user__date_joined'))
            df['user__date_joined'] = pd.to_datetime(df['user__date_joined'])
            df.set_index('user__date_joined', drop=True, inplace=True)
            customer_count = list(df.resample('D').count()['id'])
        else:
            customer_count = [0]

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
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_vendor:
            # Quick check if the user is vendor
            return redirect('not-authorized')
        method = self.request.POST.get('_method', '').lower()
        if method == 'update_points':
            return self.update_points(*args, **kwargs)
        return super(CustomersView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        customers = request.user.vendor.customers.all()
        return render(request, 'vendor/all_customers.html', locals())

    def update_points(self, request, *args, **kwargs):
        customer = get_object_or_404(Customer, pk=request.POST['pk'])
        if request.POST['type'] == 'achats':
            customer.points += round(float(request.POST['points']))
            Transaction.objects.create(vendor=request.user.vendor, customer=customer, amount=round(float(request.POST['points'])), category="A")
        else:
            customer.points -= round(float(request.POST['points']))
            Transaction.objects.create(vendor=request.user.vendor, customer=customer, amount=round(float(request.POST['points'])), category="R")
        customer.save()

        return redirect("vendor_customers")


def customers_search(request):
    url_parameter = request.GET.get("q")

    if url_parameter:
        customers = request.user.vendor.customers.filter(Q(user__first_name__icontains=url_parameter) | Q(user__last_name__icontains=url_parameter) | Q(pk__istartswith=url_parameter))
    else:
        customers = request.user.vendor.customers.all()
    html = render_to_string(
        template_name="vendor/customers_partial_results.html", 
        context={"customers": customers}
    )
    return JsonResponse({"html": html}, status=200, safe=False)


def filter_customers(data):
    queryset = Customer.objects.all()
    if data['type'] == 'points_filter':
        if data['gte']:
            queryset = queryset.filter(points__gte=data['gte'])
        if data['lte']:
            queryset = queryset.filter(points__lte=data['lte'])
    elif data['type'] == 'date_filter':
        if data['gte']:
            queryset = queryset.filter(user__date_joined__gte=data['gte'])
        if data['lte']:
            queryset = queryset.filter(user__date_joined__lte=data['lte'])
    return queryset


class CustomerListsView(LoginRequiredMixin, View):
    """
    Cette page permet de gérer au commerçant de gérer ses listes de clients (pour la diffusion email & sms)
    """
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_vendor:
            # Quick check if the user is vendor
            return redirect('not-authorized')

        method = self.request.POST.get('_method', '').lower()
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(CustomerListsView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        lists = request.user.vendor.lists.all()
        avg_lists = lists.annotate(nb_customers=Count('customers')).aggregate(Avg('nb_customers'))['nb_customers__avg']
        return render(request, 'vendor/customers_lists.html', locals())

    def post(self, request, *args, **kwargs):
        if request.POST['manual'] == 'false':
            # Automatic filtering
            queryset = list(filter_customers(request.POST))
        else:
            queryset = list(Customer.objects.filter(pk__in=request.POST['list_user'].split(',')))

        liste = CustomersList.objects.create(vendor=request.user.vendor, name=request.POST['name'])
        liste.customers.add(*queryset)
        liste.save()
        return JsonResponse({}, status=200)

    def delete(self, request, *args, **kwargs):
        liste = get_object_or_404(CustomersList, pk=request.POST['pk'])
        liste.delete()
        return JsonResponse({}, status=200)

def CustomerListsCountSelected(request):
    data = request.POST
    queryset = filter_customers(data)
    return JsonResponse({'count': queryset.count()}, status=200)

def CustomerRemoveFromList(request, list_pk, pk):
    list = get_object_or_404(CustomersList, pk=list_pk)
    customer = get_object_or_404(Customer, pk=pk)
    if not customer in list.customers.all():
        return JsonResponse({}, status=400)
    else:
        list.customers.remove(customer)
    return JsonResponse({'detail': 'OK'}, status=200)

def CustomerAddInList(request, list_pk, pk):
    list = get_object_or_404(CustomersList, pk=list_pk)
    customer = get_object_or_404(Customer, pk=pk)
    if customer in list.customers.all():
        return JsonResponse({}, status=400)
    else:
        list.customers.add(customer)
    return JsonResponse({'detail': 'OK'}, status=200)


class AnalysisView(LoginRequiredMixin, View):
    """
    Cette page permet de gérer au commerçant de gérer ses clients
    """
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_vendor:
            # Quick check if the user is vendor
            return redirect('not-authorized')
        return super(AnalysisView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        vendor = request.user.vendor
        if vendor.customers.count() > 0:
            df = pd.DataFrame(vendor.customers.values('id', 'user__date_joined'))
            df['user__date_joined'] = pd.to_datetime(df['user__date_joined'])
            df.set_index('user__date_joined', drop=True, inplace=True)
            customer_count = list(df.resample('D').count()['id'])
            customer_count_index = list(df.resample('D').count().index.strftime("%Y-%m-%d"))
        else:
            customer_count = [0]
            customer_count_index = [timezone.now().strftime("%Y-%m-%d")]

        context = {
            'customer_count': customer_count,
            'customer_count_index': customer_count_index
        }
        return render(request, 'vendor/analysis.html', context)


class DiscountsView(LoginRequiredMixin, View):
    """
    Cette page permet de récupérer les réductions et offres, d'en rajouter, de les modifier ou supprimer
    """
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_vendor:
            # Quick check if the user is vendor
            return redirect('not-authorized')

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
    Cette page permet de récupérer les informations sur les campagnes marketing en cours et à venir.
    """
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_vendor:
            # Quick check if the user is vendor
            return redirect('not-authorized')
        return super(MarketingView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        mail_campaigns = MailCampaign.objects.all().order_by('-date_published')
        sms_campaigns = SMSCampaign.objects.all().order_by('-date_published')
        nb_campaigns = MailCampaign.objects.count() + SMSCampaign.objects.count()
        futur_campaigns = MailCampaign.objects.filter(date_published__gte=timezone.now()).count() + SMSCampaign.objects.filter(date_published__gte=timezone.now()).count()
        nb_impressions_email = sum([campaign.customers_count for campaign in MailCampaign.objects.all()])
        nb_impressions_sms = sum([campaign.customers_count for campaign in SMSCampaign.objects.all()])
        nb_impressions = nb_impressions_email + nb_impressions_sms
        return render(request, 'vendor/marketing.html', locals())


class SocialView(LoginRequiredMixin, View):
    """
    Cette page permet de récupérer les stats des pages Facebook et Instagram du commerçant (via jQuery)
    Elle permet également de programmer des posts Instagram et Facebook
    """
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_vendor:
            # Quick check if the user is vendor
            return redirect('not-authorized')

        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(SocialView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        vendor = request.user.vendor
        events = []
        fb_events = [{'id': event.pk, 'title': event.description, 'start': event.date_published.strftime('%Y-%m-%d'), 'backgroundColor': '#2D88FF'} for event in list(vendor.fb_events.all())]
        ig_events = [{'id': event.pk, 'title': event.description, 'start': event.date_published.strftime('%Y-%m-%d'), 'backgroundColor': '#CA007D'} for event in list(vendor.ig_events.all())]
        events = fb_events + ig_events

        fb_today = vendor.fb_events.filter(date_published__year=timezone.now().year,date_published__month=timezone.now().month,date_published__day=timezone.now().day)
        ig_today = vendor.ig_events.filter(date_published__year=timezone.now().year,date_published__month=timezone.now().month,date_published__day=timezone.now().day)

        context = {
            'events': json.dumps(events),
            'fb_today': fb_today,
            'ig_today': ig_today
        }
        return render(request, 'vendor/social.html', context)

    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass

class SocialAddView(LoginRequiredMixin, View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_vendor:
            # Quick check if the user is vendor
            return redirect('not-authorized')

        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(SocialAddView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        vendor = request.user.vendor
        return render(request, 'vendor/create_post.html', locals())

    def post(self, request, *args, **kwargs):
        vendor = request.user.vendor
        # We first determine a publication date
        if request.POST['immediate'] == 'true':
            date_published = timezone.now()
            date_published_char = timezone.now().strftime('%d/%m/%Y %H:%M')
        else:
            date_published = timezone.make_aware(datetime.datetime.strptime(request.POST['date'], '%m/%d/%Y'), timezone.get_current_timezone())
            date_published_char = '{} {}'.format(request.POST['date'], request.POST['hour'])

        # We create an event for facebook if needed
        if request.POST['isFacebook'] == 'true':
            event = FacebookEvent.objects.create(vendor=vendor, date_published=date_published, date_published_char=date_published_char, post_type=request.POST['content_type'], description=request.POST['post_facebook'])
            event.images.add(*request.POST['fb_medias'].split(','))
            event.save()

        # We create an event for Instagram if needed
        if request.POST['isInstagram'] == 'true':
            event = InstagramEvent.objects.create(vendor=vendor, date_published=date_published, date_published_char=date_published_char, post_type=request.POST['content_type'], description=request.POST['post_instagram'])
            event.images.add(*request.POST['ig_medias'].split(','))
            event.save()

        messages.add_message(request, messages.SUCCESS, 'Le post du {} a été programmé.'.format(event.date_published_char))
        return JsonResponse({'detail': 'OK'}, status=200)


def upload_medias(request):
    form = MediaForm(request.POST, {'file' : request.FILES.getlist('file')[0]})
    if form.is_valid():
        image = form.save()
        return JsonResponse({'url': image.file.url, 'pk': image.pk}, status=201)
    else:
        return JsonResponse(form.errors.as_json(), status=400)

class TrainingView(LoginRequiredMixin, View):
    """
    Cette page permet de récupérer les principales stats sur le commerçant
    """
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_vendor:
            # Quick check if the user is vendor
            return redirect('not-authorized')
        return super(TrainingView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        trainings = Training.objects.filter(is_active=True).order_by('-date_added')
        return render(request, 'vendor/training.html', locals())


class SettingsView(LoginRequiredMixin, View):
    """
    Cette vue permet de gérer les paramètres d'une page commerçant, 
    comme la carte de fidélité liée et les informations générales du compte.
    """
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_vendor:
            # Quick check if the user is vendor
            return redirect('not-authorized')
        return super(SettingsView, self).dispatch(*args, **kwargs)

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


class HelpView(LoginRequiredMixin, View):
    """
    Cette page permet d'envoyer des messages d'assistance au support
    """
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_vendor:
            # Quick check if the user is vendor
            return redirect('not-authorized')
        return super(HelpView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'vendor/help.html', locals())

    def post(self, request, *args, **kwargs):
        form = p(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.vendor = request.user.vendor
            message.save()
            messages.add_message(request, messages.SUCCESS, 'Votre message a été envoyé. Il sera traité dans les plus brefs délais.')
        else:
            errors = json.loads(form.errors.as_json())
            for error in errors:
                messages.add_message(request, messages.ERROR, '{}: {}'.format(error, errors[error][0]['message']))
        return redirect('vendor_help')



class NewEmailingView(LoginRequiredMixin, View):
    """
    Cette page permet d'ajouter une nouvelle campagne d'emailing
    """
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_vendor:
            # Quick check if the user is vendor
            return redirect('not-authorized')
        return super(NewEmailingView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'vendor/new_emailing.html', locals())

    def post(self, request, *args, **kwargs):
        form = MailCampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.vendor = request.user.vendor
            campaign.save()

            # We increment list counters
            if request.POST['to_everyone'] != 'true':
                for liste in request.POST['lists'].split(','):
                    liste.mail_campaigns.add(campaign)
                    liste.save()

            # Add logic to send mass mailing
            current_site = get_current_site(request)
            mail_subject = campaign.subject

            mails = []
            if request.POST['to_everyone'] == 'true':
                list_receivers = list(request.user.vendor.customers.all())
            else:
                for liste in request.POST['lists'].split(','):
                    list_receivers.append(*list(liste.customers.all()))
             
            for customer in list_receivers:
                message = render_to_string('emails/information_mail.html', {
                    'customer': customer,
                    'media': campaign.image,
                    'content': campaign.content,
                    'domain': current_site.domain,
                    'vendor': request.user.vendor
                })
                mails.append((mail_subject, campaign.content, message, 'no-reply@app.kustomr.fr', [customer.user.email]))

            send_mass_html_mail(mails)

        else:
            return JsonResponse({}, status=400)
        return JsonResponse({}, status=200)


class NewSMSView(LoginRequiredMixin, View):
    """
    Cette page permet d'ajouter une nouvelle campagne de SMS
    """
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_vendor:
            # Quick check if the user is vendor
            return redirect('not-authorized')
        return super(NewSMSView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'vendor/new_sms.html', locals())

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = SMSCampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.vendor = request.user.vendor
            campaign.save()

            # Send the SMS to Twilio here
        else:
            return JsonResponse({}, status=400)
        return JsonResponse({}, status=200)


class ArticlesView(LoginRequiredMixin, View):
    """
    Cette page permet de gérer au commerçant de gérer ses clients
    """
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_vendor:
            # Quick check if the user is vendor
            return redirect('not-authorized')
        method = self.request.POST.get('_method', '').lower()
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(ArticlesView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        vendor = request.user.vendor
        articles = vendor.articles.all()
        return render(request, 'vendor/articles.html', locals())

    def post(self, request, *args, **kwargs):
        vendor = request.user.vendor
        formMedia = MediaForm(request.POST, request.FILES)
        if formMedia.is_valid():
            media = formMedia.save()
            form = ArticleForm(request.POST)
            if form.is_valid():
                article = form.save(commit=False)
                article.vendor = vendor
                article.image = media
                article.save()
                messages.add_message(request, messages.SUCCESS, 'L\'article a été publié.')
            else:
                errors = json.loads(form.errors.as_json())
                for error in errors:
                    messages.add_message(request, messages.ERROR, '{} : {}'.format(error, errors[error][0]['message']))
        else:
            errors = json.loads(formMedia.errors.as_json())
            for error in errors:
                messages.add_message(request, messages.ERROR, '{} : {}'.format(error, errors[error][0]['message']))
        return redirect('vendor_articles')

    def delete(self, request, *args, **kwargs):
        obj = get_object_or_404(Article, pk=request.POST['pk'])
        messages.add_message(request, messages.SUCCESS, 'L\'article "{}" a été supprimée.'.format(obj.title))
        obj.delete()
        return redirect('vendor_articles')


def CustomerById(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    data = model_to_dict(customer.user)
    return JsonResponse({'customer': model_to_dict(customer), 'user': model_to_dict(customer.user)}, status=200)