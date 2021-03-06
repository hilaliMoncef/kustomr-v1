from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name="admin_home"),
    path('vendors', views.VendorsView.as_view(), name="admin_vendors"),
    path('socials', views.SocialsView.as_view(), name="admin_socials"),
    path('socials/facebook/<int:pk>/toggle', views.toggle_fb_processed, name="admin_facebook_toggle"),
    path('socials/instagram/<int:pk>/toggle', views.toggle_ig_processed, name="admin_instagram_toggle"),
    path('marketings', views.MarketingView.as_view(), name="admin_marketings"),
    path('marketings/sms/<int:pk>/toggle', views.toggle_sms_processed, name="admin_sms_toggle"),
    path('marketings/email/<int:pk>/toggle', views.toggle_email_processed, name="admin_email_toggle"),
    path('formations', views.TrainingsView.as_view(), name="admin_trainings"),
    path('messages', views.MessagesView.as_view(), name="admin_messages"),
    path('messages/<int:pk>/read', views.read_message, name="admin_read_message"),
    path('messages/<int:pk>/delete', views.delete_message, name="admin_delete_message")
]
