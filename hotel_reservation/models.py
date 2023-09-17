from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    ROOM_TYPE_CHOICES = (
        ('single', 'single'),
        ('double', 'double'),
        ('suite', 'suite'),
    )

    room_number = models.PositiveIntegerField(unique=True)
    room_type = models.CharField(max_length=50, choices=ROOM_TYPE_CHOICES)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return str(self.room_number)


class Reservation(models.Model):
    room = models.ForeignKey(Room, related_name='reservations', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reservations', on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()

    def __str__(self):
        return f'reserved from {self.check_in_date} to {self.check_out_date}'
