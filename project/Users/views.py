from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.http import Http404


class LoginView(View):
    """
    Cette page permet la connexion d'un utilisateur traditionnel (commerçant ou administrateur)
    """
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request, 'generics/login.html', locals())

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_active:
                if user.is_vendor:
                    login(request, user)
                    messages.add_message(request, messages.SUCCESS, 'Vous êtes connecté.')
                    return redirect('vendor_home')
                elif user.is_customer:
                    login(request, user)
                    messages.add_message(request, messages.SUCCESS, 'Vous êtes connecté.')
                    return redirect('customer_home')
                elif user.is_staff:
                    login(request, user)
                    messages.add_message(request, messages.SUCCESS, 'Vous êtes connecté.')
                    return redirect('admin_home')
                else:
                    raise Http404()
            else:
                messages.add_message(request, messages.ERROR, 'Cet utilisateur est désactivé.')
        else:
            messages.add_message(request, messages.ERROR, 'Impossible de trouver un utilisateur avec ces identifiants.')
        return render(request, 'generics/login.html', locals())


class LogoutView(View):
    """
    Cette vue permet de déconnecter n'importe quel utilisateur. Elle ne renvoit aucune erreur.
    """
    def get(self, request, vendor=None, *args, **kwargs):
        if request.user.is_customer and vendor:
            vendor = request.user.get_customer(store=vendor).store_linked
            logout(request)
            return redirect('customer_landing_page', vendor=vendor.pk, store_name=vendor.store_name)
        else:
            logout(request)
            return redirect('login')