import datetime

from django.http import JsonResponse
from django.views.generic import CreateView, DetailView, UpdateView

from rest_framework import generics, serializers

import utils
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
        # @TODO: Get idea how to do it with SQL
        for date in utils.date_range(serializer.validated_data['arrival_date'],
                                     serializer.validated_data['departure_date']):
            if Reservation.objects.for_date(date).count() >= config.max_rooms:
                raise serializers.ValidationError({'error': 'No rooms available.'})
            date += datetime.timedelta(days=1)
        serializer.save()
