from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404


@login_required
def index(request):
    if request.user.is_staff:
        return redirect('admin_home')
    elif request.user.is_vendor:
        return redirect('vendor_home')
    elif request.user.is_customer:
        return redirect('logout')
    else:
        raise Http404()


def not_authorized(request):
    return render(request, 'generics/not-authorized.html', locals())

def legal(request):
    return render(request, 'generics/legal.html', locals())

def handler404(request, exception, template_name="generics/404.html"):
    response = render(request, template_name)
    response.status_code = 404
    return response

def handler500(request, template_name="generics/500.html"):
    response = render(request, template_name)
    response.status_code = 500
    return response