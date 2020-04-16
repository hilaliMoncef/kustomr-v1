from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include('Admin.urls')),
    path('', views.index, name="home"),
    path('users/', include('Users.urls')),
    path('vendor/', include('Vendor.urls')),
    path('customer/', include('Customer.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)