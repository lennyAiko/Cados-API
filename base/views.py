from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

# don't deploy with sqlite

@api_view(['GET'])
def endpoints(req):
    data = ['/advocates', 'advocates/:username']
    return Response(data)

def advocate_list(req):
    data = ['Dennis', 'Lennox', 'Max', 'Tadas']
    return JsonResponse(data, safe=False)

def advocate_detail(req, username):
    data = username
    return JsonResponse(data, safe=False)