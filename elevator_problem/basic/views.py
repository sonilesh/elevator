from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from . import models
from . import serializers
from .helpers import *
# Create your views here.


@api_view(['GET'])
def get_routes(request):
    '''
    api for displaying the available endpoints with body, method, description
    '''
    routes = [
        {
            "endpoint": "/elevator/",
            "method": "POST",
            "body": {
                "count" : "n",

            },
            "description": "Create n new elevators"
        },
    ]
    return Response(routes)


@api_view(['POST'])
def create_elevators(request):
    elevators = []
    data = request.data
    count = data["count"]
    try:
        for _ in range(count):
            elevator = models.Elevator.objects.create()
            elevators.append(elevator.ID)
        response = {
            "elevators": elevators,
            "message":  "Elevators are successfully created"   
        }
    except:
        response = {
            "elevators": elevators,
            "message":  "Failed to create elevators"   
        }
    return Response(response)


@api_view(['PUT'])
def open_door(request, pk):
    elevator = get_object_or_404(models.Elevator, id = pk)
    data = {"door_status": OPEN}
    serializer = serializers.ElevatorSerializer(elevator, data = data, partial = True)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response("Invalid data found", status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data)

@api_view(['PUT'])
def close_door(request, pk):
    elevator = get_object_or_404(models.Elevator, id = pk)
    data = {"door_status": CLOSE}
    serializer = serializers.ElevatorSerializer(elevator, data = data, partial = True)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response("Invalid data found", status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data)

@api_view(['PUT'])
def mark_lift_not_operational(request, pk):
    elevator = get_object_or_404(models.Elevator, id = pk)
    data = {"operational": False}
    serializer = serializers.ElevatorSerializer(elevator, data = data, partial = True)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response("Invalid data found", status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data)

@api_view(['POST'])
def make_request(request, pk):
    elevator = get_object_or_404(models.Elevator, id = pk)
    data = request.data
    user_request = models.UserRequest.objects.create(
        elevator = elevator,
        requested_floor = data["floor"],
    )
    serializer = serializers.UserRequestSerializer(user_request, many=False)
    return Response(serializer.data)
