import datetime

from django.http import JsonResponse
from django.views.generic import CreateView, DetailView, UpdateView

from rest_framework import generics, serializers

from .models import HotelConfig, Reservation
from .serializers import ConfigSerializer, ReservationSerializer


class ConfigView(generics.RetrieveUpdateAPIView):
    serializer_class = ConfigSerializer

    def get_object(self):
        return HotelConfig.get_config()

class ReservationView(generics.CreateAPIView):
    serializer_class = ReservationSerializer
    # @TODO: Not sure why it needs queryset. It's not used it explicitly
    queryset = Reservation.objects.all()

    def perform_create(self, serializer):
        config = HotelConfig.get_config()
        max_occupied = Reservation.objects.max_occupied(
            serializer.validated_data['arrival_date'],
            serializer.validated_data['departure_date'])
        if max_occupied >= config.max_rooms:
            raise serializers.ValidationError({'error': 'No rooms available.'})
        serializer.save()
