from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.DashboardView.as_view(), name="vendor_home"),
    path('customer/new', views.NewCustomerView.as_view(), name="vendor_new_customer"),
]
