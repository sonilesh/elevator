from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from . import models
from . import serializers
from .helpers import *
import threading
import time


### Assumptions :

# 1. lift takes 1 sec to move 1 floor (up/down)
# 2. door open/close takes 3 secs
# 3. door will automatically closed after 5 secs if doors are already opened.


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
    if elevator['running_status'] == STOP and elevator['door_status'] == CLOSE:              ### add condition for checking if lift is moving or not
        data = {"door_status": OPEN}
        serializer = serializers.ElevatorSerializer(elevator, data = data, partial = True)
        if serializer.is_valid():
            print("Opening the lift!!!")
            time.sleep(3)                                                                    ### added time of 3 secs to open lift
            serializer.save()
            close_thread = threading.Timer(5, close_door_helper(elevator))                   ### after 5 secs doors will automatically closed
            close_thread.start()
        else:
            return Response("Invalid data found", status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)
    else:
        return Response("Lift is moving hence not able to open the door!!")

def close_door_helper(elevator):
    if elevator['running_status'] == STOP and elevator['door_status'] == OPEN:                 ### condition to check if lift is not moving and doors are open
        data = {"door_status": CLOSE}
        serializer = serializers.ElevatorSerializer(elevator, data = data, partial = True)
        if serializer.is_valid():
            print("Closing the lift!!")
            time.sleep(3)                                                                       ### added time of 3 secs to close the lift
            serializer.save()
        else:
            return Response("Invalid data found", status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)
    else:
        return Response("Lift is moving hence doors are already closed!!")

@api_view(['PUT'])
def close_door(request, pk):
    elevator = get_object_or_404(models.Elevator, id = pk)
    return close_door_helper(elevator)

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

@api_view(['GET'])
def next_floor(request, pk):
    req = models.Elevator.objects.get(elevator = pk)
    if req:
        return req["next_floor"]

    return Response("There is no lift with this id!!!")

@api_view(['GET'])
def fetch_all_request_of_lift(request, pk):
    req = models.UserRequest.objects.get(elevator = pk)
    if not len(req):
        return Response("There is no request made hence next floor can't be calculated")
    serializer = UserRequestSerializer(req, many=True)
    return Response(serializer.data)
 
@api_view(['GET'])
def fetch_direction(request, pk):
    req = models.Elevator.objects.get(elevator = pk)
    if req:
        return req["lift_requested_direction"] if req["lift_requested_direction"] else req["initial_direction"]

    return Response("There is no lift with this id!!!")


@api_view(['POST'])
def make_request(request, pk):
    # 1. Add request to the lift
    # 2. Update the next destination of the lift
    # 3. Keep checking the requests for next destination after every seconds
    elevator = get_object_or_404(models.Elevator, id = pk)
    data = request.data
    user_request = models.UserRequest.objects.create(
        elevator = elevator,
        requested_floor = data["floor"]
    )
    serializer = serializers.UserRequestSerializer(user_request, many=False)
    process_request_thread = threading.Thread(process_request)
    process_request_thread.start()
    return Response(serializer.data)

@api_view(['POST'])
def call_lift(request):
    # 1. find out which lift needs to be called/assigned to user
    # 2. Add request to the lift
    # 3. Update the next destination of the lift
    # 4. Keep checking the requests for next destination after every seconds
    pass

def process_request():
    # sort the requests and move lift by one floor and check all request again if request comes with same direction or not.
    pass

