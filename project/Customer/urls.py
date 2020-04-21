from django.urls import path
from . import views

urlpatterns = [
    path('welcome/<int:vendor>-<str:store_name>', views.LandingPageView.as_view(), name="customer_landing_page"),
    path('dashboard/<int:vendor>-<str:store_name>/<str:token>', views.DashboardView.as_view(), name="customer_home"),
]
