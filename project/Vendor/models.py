from django.db import models
from Users.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import os


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

    # Store infos
    store_phone = models.CharField(blank=True, null=True, max_length=255)
    store_adress = models.TextField(blank=True, null=True)

    # Social links
    website = models.CharField(max_length=255, default='', null=True, blank=True)
    facebook = models.CharField(max_length=255, default='', null=True, blank=True)
    instagram = models.CharField(max_length=255, default='', null=True, blank=True)
    youtube = models.CharField(max_length=255, default='', null=True, blank=True)
    linkedin = models.CharField(max_length=255, default='', null=True, blank=True)
    pinterest = models.CharField(max_length=255, default='', null=True, blank=True)
    snapchat = models.CharField(max_length=255, default='', null=True, blank=True)
    tripadvisor = models.CharField(max_length=255, default='', null=True, blank=True)

    def __str__(self):
        return self.store_name

    @property
    def nb_clients(self):
        print(self.customers.all().count())
        return self.customers.all().count()


class VendorOpeningHours(models.Model):
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE, related_name="opening_hours")
    monday = models.CharField(max_length=100, blank=True, default="-")
    tuesday = models.CharField(max_length=100, blank=True, default="-")
    wednesday = models.CharField(max_length=100, blank=True, default="-")
    thursday = models.CharField(max_length=100, blank=True, default="-")
    friday = models.CharField(max_length=100, blank=True, default="-")
    saturday = models.CharField(max_length=100, blank=True, default="-")
    sunday = models.CharField(max_length=100, blank=True, default="-")

    def __str__(self):
        return 'Heures d\'ouvertures de {}'.format(self.vendor.store_name)


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
        This function is connected to Vendor Modeal creation to create a default RewardCardLayout and a default Opening Hours
    """
    if created:
        VendorOpeningHours.objects.create(vendor=instance)
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


def get_ig_upload_path(instance, filename):
    """
    Helper function to get custom path for vendor's uploaded files for INSTAGRAM
    """
    print(os.path.join("posts", "instagram", "user_%d" % instance.vendor.pk, filename))
    return os.path.join("posts", "instagram", "user_%d" % instance.vendor.pk, filename)

def get_fb_upload_path(instance, filename):
    """
    Helper function to get custom path for vendor's uploaded files for INSTAGRAM
    """
    print(os.path.join("posts", "instagram", "user_%d" % instance.vendor.pk, filename))
    return os.path.join("posts", "instagram", "user_%d" % instance.vendor.pk, filename)


def get_social_upload_path(instance, filename):
    """
    Helper function to get custom path for vendor's uploaded files for INSTAGRAM
    """
    print(os.path.join("posts", "instagram", "user_%d" % instance.vendor.pk, filename))
    return os.path.join("posts", "instagram", "user_%d" % instance.vendor.pk, filename)


class SocialMedia(models.Model):
    file = models.FileField(upload_to='posts/medias/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'File uploaded at {}'.format(self.uploaded_at)


class InstagramEvent(models.Model):
    """
    This model represents an event on instagram
    """
    # Choices for store type
    POST_TYPE_CHOICES = [
        ('S', 'Story'),
        ('P', 'Post'),
    ]

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="ig_events")
    images = models.ManyToManyField(SocialMedia, related_name="ig_events")
    description = models.TextField()
    post_type = models.CharField(max_length=40, choices=POST_TYPE_CHOICES, default='P')
    processed = models.BooleanField(default=False)
    date_processed = models.DateTimeField(blank=True, null=True)
    date_published_char = models.CharField(max_length=255)
    date_published = models.DateTimeField()

    def __str__(self):
        return 'Insta post on {} for {}'.format(self.date_published, self.vendor.store_name)

class FacebookEvent(models.Model):
    """
    This model represents an event on Facebook
    """
    # Choices for store type
    POST_TYPE_CHOICES = [
        ('S', 'Story'),
        ('P', 'Post'),
    ]

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="fb_events")
    images = models.ManyToManyField(SocialMedia, related_name="fb_events")
    description = models.TextField()
    post_type = models.CharField(max_length=40, choices=POST_TYPE_CHOICES, default='P')
    processed = models.BooleanField(default=False)
    date_processed = models.DateTimeField(blank=True, null=True)
    date_published_char = models.CharField(max_length=255)
    date_published = models.DateTimeField()

    def __str__(self):
        return 'Facebook post on {} for {}'.format(self.date_published, self.vendor.store_name)