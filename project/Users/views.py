from django.shortcuts import render

# Create your views here.

def login(request):
    """
    Cette page permet la connexion d'un utilisateur traditionnel (commerçant ou administrateur)
    """
    return render(request, 'templates/generics/login.html', locals())