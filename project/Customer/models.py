from django.db import models
from Users.models import User
from Vendor.models import Vendor


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer")
    store_linked = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="customers")
    points = models.IntegerField(default=0)

    def __str__(self):
        return 'Customer : {}'.format(self.user)