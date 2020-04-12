from django.contrib import messages
from Users.models import Vendor
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View


class LandingPageView(View):
    """
    Cette page permet de récupérer les principales stats sur le commerçant
    """
    def get(self, request, *args, **kwargs):
        vendor = get_object_or_404(Vendor, pk=self.kwargs['vendor'])
        return render(request, 'landing_page.html', locals())