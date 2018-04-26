from django.db import models


class HotelConfig(models.Model):
    rooms = models.SmallIntegerField()
    overbooking = models.SmallIntegerField()

    @property
    def max_rooms(self):
        return self.rooms + self.rooms * self.overbooking // 100

    # @TODO: custom object manager?
    @classmethod
    def get_config(cls):
        config = cls.objects.first()
        if config is None:
            config = cls.objects.create(rooms=100, overbooking=0)
        return config


class Reservation(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField()
    arrival_date = models.DateField()
    departure_date = models.DateField()
