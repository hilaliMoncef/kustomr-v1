from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="home"),
    path('users/', include('Users.urls')),
    path('vendor/', include('Vendor.urls')),
    path('customer/', include('Customer.urls'))
]
