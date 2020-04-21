from django.db import models
from Users.models import User
from Vendor.models import Vendor
from django.db.models.signals import post_save
from django.dispatch import receiver


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


@receiver(post_save, sender=Customer)
def save_token(sender, instance, created, **kwargs):
    if created:
        from secrets import token_urlsafe
        instance.token = CustomerToken.objects.create(token=token_urlsafe(20))
        instance.save()