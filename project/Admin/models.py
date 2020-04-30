from django.db import models
from Vendor.models import Vendor


class Training(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    is_free = models.BooleanField(default=False)
    link = models.CharField(max_length=400)
    poster = models.FileField(upload_to='tranings/posters/', default=None, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    vendor = models.ForeignKey(Vendor, default='Unknown', on_delete=models.SET_DEFAULT)
    subject = models.CharField(max_length=255)
    date_sent = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    read = models.BooleanField(default=False)
    responded = models.BooleanField(default=False)

    def __str__(self):
        return 'Message from {} : {}'.format(self.vendor.store_name, self.subject)

    