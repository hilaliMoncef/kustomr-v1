from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include('Admin.urls')),
    path('not-authorized', views.not_authorized, name="not-authorized"),
    path('', views.index, name="home"),
    path('legal', views.legal, name="legal"),
    path('users/', include('Users.urls')),
    path('vendor/', include('Vendor.urls')),
    path('customer/', include('Customer.urls'))
    
]

handler404 = 'project.views.handler404'
handler500 = 'project.views.handler500'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)