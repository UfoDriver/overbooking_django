from django.http import JsonResponse
from django.views.generic import CreateView, DetailView, UpdateView

from rest_framework import generics, serializers

from .models import HotelConfig, Reservation
from .serializers import ConfigSerializer, ReservationSerializer


class ConfigView(generics.RetrieveUpdateAPIView):
    serializer_class = ConfigSerializer

    def get_object(self):
        # @TODO: overbooking decrease checking
        return HotelConfig.get_config()


class ReservationView(generics.CreateAPIView):
    serializer_class = ReservationSerializer
    # Not sure why it needs queryset. We don't use it explicitly
    queryset = Reservation.objects.all()
    # @TODO: check if we can book on that date

    def perform_create(self, serializer):
        config = HotelConfig.get_config()
        # Cannot imagine sql right now, making it with python
        serializer.validated_data['arrival_date']
        serializer.validated_data['departure_date']

        # raise serializers.ValidationError('OMG')
        serializer.save()
