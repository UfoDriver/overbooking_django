from django.urls import path

from . import views


urlpatterns = [
    path(r'config', views.ConfigView.as_view()),
    path(r'reservations', views.ReservationView.as_view()),
]
