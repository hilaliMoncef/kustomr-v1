from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.DashboardView.as_view(), name="vendor_home"),
    path('settings', views.SettingsView.as_view(), name="vendor_settings"),
    path('help', views.HelpView.as_view(), name="vendor_help"),
    path('customers', views.CustomersView.as_view(), name="vendor_customers"),
    path('customers/points/add', views.DashboardView.as_view(), name="vendor_add_points"),
    path('customer/new', views.NewCustomerView.as_view(), name="vendor_new_customer"),
    path('discounts', views.DiscountsView.as_view(), name="vendor_discounts"),
    path('marketing', views.MarketingView.as_view(), name="vendor_marketing"),
    path('analysis', views.AnalysisView.as_view(), name="vendor_analysis"),
    path('social', views.SocialView.as_view(), name="vendor_social"),
    path('social/media/upload', views.upload_medias, name="vendor_social_upload_media"),
    path('social/new', views.SocialAddView.as_view(), name="vendor_social_add"),
    path('training', views.TrainingView.as_view(), name="vendor_training"),
]
