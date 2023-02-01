from rest_framework.serializers import ModelSerializer
from . import models

class ElevatorSerializer(ModelSerializer):
    class Meta:
        model = models.Elevator
        fields = "__all__"

class UserRequestSerializer(ModelSerializer):
    class Meta:
        model = models.UserRequest
        fields = "__all__"