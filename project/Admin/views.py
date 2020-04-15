from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, View):
    """
    Cette page permet de récupérer les principales stats sur le commerçant
    """
    def get(self, request, *args, **kwargs):
        return render(request, 'admin/home.html', locals())
