from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.DashboardView.as_view(), name="vendor_home"),
    path('settings', views.SettingsView.as_view(), name="vendor_settings"),
    path('customers', views.DashboardView.as_view(), name="vendor_customers"),
    path('customers/points/add', views.DashboardView.as_view(), name="vendor_add_points"),
    path('customer/new', views.NewCustomerView.as_view(), name="vendor_new_customer"),
]
