from django.db import models
from .helpers import *

# Create your models here.

class Elevator(models.Model):
    current_floor = models.IntegerField(default = 0)
    next_floor = models.IntegerField()
    running_status = models.CharField(max_length = 5, choices = RUNNING_STATUS_CHOICES, default = STOP)
    operational = models.BooleanField(default = True)
    door_status = models.CharField(max_length = 5, choices = DOOR_STATUS_CHOICES, default = CLOSE)
    direction = models.CharField(max_length = 4, choices = DIRECTION_CHOICES, default = UP)


class UserRequest(models.Model):
    elevator = models.ForeignKey('Elevator', on_delete = models.CASCADE)
    requested_floor = models.IntegerField(null = False)

    def __str__(self):
        return "Requested " + self.elevator.id + " for " + self.requested_floor


