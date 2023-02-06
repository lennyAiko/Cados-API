from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Advocate
from .serializers import AdvocateSerializer

# Create your views here.

# don't deploy with sqlite

@api_view(['GET'])
def endpoints(req):
    data = ['/advocates', 'advocates/:username']
    return Response(data)

@api_view(['GET'])
def advocate_list(req):
    # data = ['Dennis', 'Lennox', 'Max', 'Tadas']
    advocates = Advocate.objects.all()
    serializer = AdvocateSerializer(advocates, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def advocate_detail(req, username):
    advocate = Advocate.objects.get(username=username)
    serializer = AdvocateSerializer(advocate, many=False)
    return Response(serializer.data)