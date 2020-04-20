from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.DashboardView.as_view(), name="vendor_home"),
    path('settings', views.SettingsView.as_view(), name="vendor_settings"),
    path('customers', views.CustomersView.as_view(), name="vendor_customers"),
    path('customers/points/add', views.DashboardView.as_view(), name="vendor_add_points"),
    path('customer/new', views.NewCustomerView.as_view(), name="vendor_new_customer"),
    path('discounts', views.DiscountsView.as_view(), name="vendor_discounts"),
    path('marketing', views.MarketingView.as_view(), name="vendor_marketing"),
    path('social', views.SocialView.as_view(), name="vendor_social"),
]
