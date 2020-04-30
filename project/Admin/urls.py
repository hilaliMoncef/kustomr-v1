from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name="admin_home"),
    path('vendors', views.VendorsView.as_view(), name="admin_vendors"),
    path('formations', views.TrainingsView.as_view(), name="admin_trainings")
]
