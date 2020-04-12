from django.urls import path
from . import views

urlpatterns = [
    path('welcome/<int:vendor>-<str:store_name>', views.LandingPageView.as_view(), name="customer_landing_page"),
]
