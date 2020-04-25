from django.db import models


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
