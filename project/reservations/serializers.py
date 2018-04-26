import datetime

from rest_framework import serializers

from . import models


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelConfig
        fields = ('rooms', 'overbooking')

    def validate_rooms(self, room_number):
        if room_number <= 0:
            raise serializers.ValidationError('Room number cannot be less than one.')
        return room_number

    def validate_overbooking(self, overbooking):
        if overbooking < 0:
            raise serializers.ValidationError('Overbooking cannot be negative.')
        return overbooking

    def validate(self, data):
        new_max_number = data['rooms'] + data['rooms'] * data['overbooking'] // 100
        if models.Reservation.objects.max_occupied() > new_max_number:
            raise serializers.ValidationError('Cannot decrease room number or overbooking number.')
        return data


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reservation
        fields = ('name', 'email', 'arrival_date', 'departure_date')

    def validate_arrival_date(self, date):
        if date < datetime.date.today():
            raise serializers.ValidationError('Cannot set arrival date in the past.')
        return date

    def validate(self, data):
        if data['arrival_date'] > data['departure_date']:
            raise serializers.ValidationError('Departure date must occur after arrival date.')
        return data
