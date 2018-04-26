from django.urls import path

from . import views

app_name = 'reservations'
urlpatterns = [
    path(r'config', views.ConfigView.as_view(), name='config'),
    path(r'reservations', views.ReservationView.as_view(), name='reservations'),
]
