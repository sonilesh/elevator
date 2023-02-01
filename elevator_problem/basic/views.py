from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
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

