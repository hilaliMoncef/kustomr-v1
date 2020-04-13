from django.db import models
from Users.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Vendor(models.Model):
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

    def __str__(self):
        return self.store_name