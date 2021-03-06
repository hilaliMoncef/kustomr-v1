from django.db import models
from Users.models import User
from Vendor.models import Vendor, MailCampaign
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class CustomerToken(models.Model):
    token = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.token


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customers")
    token = models.OneToOneField(CustomerToken, on_delete=models.CASCADE, related_name="customer", default=None, blank=True, null=True)
    imported = models.BooleanField(default=False)
    store_linked = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="customers")
    points = models.IntegerField(default=0)

    def __str__(self):
        return 'Customer : {}'.format(self.user)

    @property
    def next_gift(self):
        discounts = list(self.store_linked.discounts.filter(is_active=True, end_date__gte=timezone.now(), min_points__gt=self.points).values_list('min_points', flat=True))
        offers = list(self.store_linked.offers.filter(is_active=True, end_date__gte=timezone.now(), cost__gt=self.points).values_list('cost', flat=True))
        all_points = discounts + offers or [0]
        return min(all_points) - self.points


@receiver(post_save, sender=Customer)
def save_token(sender, instance, created, **kwargs):
    if created:
        from secrets import token_urlsafe
        instance.token = CustomerToken.objects.create(token=token_urlsafe(20))
        instance.save()


class CustomersList(models.Model):
    name = models.CharField(max_length=255)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="lists")
    customers = models.ManyToManyField(Customer, related_name="lists")
    mail_campaigns = models.ManyToManyField(MailCampaign, related_name="lists")
    sms_campaigns = models.ManyToManyField(MailCampaign, related_name="sms_lists")
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Liste {}'.format(self.name)


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('A', 'Achat'),
        ('R', 'Remboursement')
    ]

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="transactions")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="transactions")
    category = models.CharField(max_length=1, choices=TRANSACTION_TYPES, default='A')
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} pour {} chez {} le {}'.format(self.category, self.customer.user, self.vendor.store_name, self.date)