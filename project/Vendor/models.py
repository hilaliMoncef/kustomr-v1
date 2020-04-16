from django.db import models
from Users.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Vendor(models.Model):
    """
        This model represents the Store manager. It is linked to a regular user account.
    """
    # Choices for store type
    STORE_TYPE_CHOICES = [
        ('FOOD', 'Restaurant & bar'),
        ('SUPERMARKET', 'Supermarché'),
    ]
    # Choices for store type
    STORE_TYPES_VISITS_CHOICES = [
        ('SM', 'Entre 50 et 200'),
        ('MD', 'Entre 200 et 500'),
        ('LG', 'Entre 500 et 1000'),
        ('XL', '1000+'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="vendor")
    store_name = models.CharField(max_length=255)
    store_type = models.CharField(max_length=40, choices=STORE_TYPE_CHOICES, default='FOOD')
    store_visits = models.CharField(max_length=40, choices=STORE_TYPES_VISITS_CHOICES, default="SM")

    # Social links
    facebook = models.CharField(max_length=255, default=None, null=True, blank=True)
    instagram = models.CharField(max_length=255, default=None, null=True, blank=True)
    tripadvisor = models.CharField(max_length=255, default=None, null=True, blank=True)

    def __str__(self):
        return self.store_name


class RewardCardLayout(models.Model):
    """
        This model represents a design of vendor's reward card, it will be used with Apple Wallet.
    """
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE, null=True, blank=True, related_name="reward_card_layout")
    icon = models.FileField(upload_to='fidelity/icons/', default=None, null=True, blank=True)
    logo = models.FileField(upload_to='fidelity/logos/', default=None, null=True, blank=True)
    bg_color = models.CharField(max_length=6, default="000000")
    text_color = models.CharField(max_length=6, default="ffffff")

    def __str__(self):
        return 'Fidelity Card Layout for {}'.format(self.vendor)


@receiver(post_save, sender=Vendor)
def create_default_layout(sender, instance, **kwargs):
    """
        This function is connected to Vendor Modeal creation to create a default RewardCardLayout
    """
    if instance.created:
        RewardCardLayout.objects.create(vendor=instance)




class Discount(models.Model):
    """
        This model represents all discounts created by the Vendor. They can be applied to the Customers.
    """
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    expiry = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return '{} - Expire le {}'.format(self.name, self.expiry)
