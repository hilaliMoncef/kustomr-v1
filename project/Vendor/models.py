from django.db import models
from Users.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

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
    website = models.CharField(max_length=255, default=None, null=True, blank=True)
    facebook = models.CharField(max_length=255, default=None, null=True, blank=True)
    instagram = models.CharField(max_length=255, default=None, null=True, blank=True)
    youtube = models.CharField(max_length=255, default=None, null=True, blank=True)
    linkedin = models.CharField(max_length=255, default=None, null=True, blank=True)
    pinterest = models.CharField(max_length=255, default=None, null=True, blank=True)
    snapchat = models.CharField(max_length=255, default=None, null=True, blank=True)
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
    bg_color = models.CharField(max_length=7, default="#000000")
    text_color = models.CharField(max_length=7, default="#ffffff")

    def __str__(self):
        return 'Fidelity Card Layout for {}'.format(self.vendor)


@receiver(post_save, sender=Vendor)
def create_default_layout(sender, instance, created, **kwargs):
    """
        This function is connected to Vendor Modeal creation to create a default RewardCardLayout
    """
    if created:
        RewardCardLayout.objects.create(vendor=instance)




class Discount(models.Model):
    """
        This model represents all discounts created by the Vendor. They can be applied to the Customers.
    """
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="discounts")
    image = models.FileField(default=None, blank=True, null=True, upload_to="discounts/")
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    min_points = models.IntegerField(default=0)
    start_date = models.DateTimeField(default=None, null=True, blank=True)
    end_date = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return 'Réduction "{}" - {}'.format(self.name, self.status_text)

    @property
    def status_text(self):
        if self.is_active:
            if timezone.now() >= self.start_date and timezone.now() <= self.end_date:
                return 'Actif'
            elif timezone.now() < self.start_date:
                return 'A venir'
            else:
                return 'Expiré'
        else:
            return 'Désactivé'
        


class Offer(models.Model):
    """
        This model represents all offers created by the Vendor. They can be applied to the Customers using customers points.
    """
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="offers")
    image = models.FileField(default=None, blank=True, null=True, upload_to="offers/")
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    cost = models.IntegerField()
    start_date = models.DateTimeField(default=None, null=True, blank=True)
    end_date = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return 'Offre "{}" - {}'.format(self.name, self.status_text)

    @property
    def status_text(self):
        if self.is_active:
            if timezone.now() >= self.start_date and timezone.now() <= self.end_date:
                return 'Actif'
            elif timezone.now() < self.start_date:
                return 'A venir'
            else:
                return 'Expiré'
        else:
            return 'Désactivé'