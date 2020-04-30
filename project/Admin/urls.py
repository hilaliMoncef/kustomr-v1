from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name="admin_home"),
    path('vendors', views.VendorsView.as_view(), name="admin_vendors"),
    path('socials', views.SocialsView.as_view(), name="admin_socials"),
    path('socials/facebook/<int:pk>/toggle', views.toggle_fb_processed, name="admin_facebook_toggle"),
    path('socials/instagram/<int:pk>/toggle', views.toggle_ig_processed, name="admin_instagram_toggle"),
    path('formations', views.TrainingsView.as_view(), name="admin_trainings")
]
