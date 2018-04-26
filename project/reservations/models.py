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


class ReservationManager(models.Manager):
    def for_date(self, date):
        return self.get_queryset().filter(arrival_date__lte=date,
                                          departure_date__gte=date)


class Reservation(models.Model):
    objects = ReservationManager()

    name = models.CharField(max_length=128)
    email = models.EmailField()
    arrival_date = models.DateField()
    departure_date = models.DateField()

    def __str__(self):
        return '{} ({}) {} - {}'.format(self.name, self.email, self.arrival_date,
                                        self.departure_date)
