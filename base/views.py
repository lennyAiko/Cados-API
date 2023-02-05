from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def endpoints(req):
    data = ['/advocates', 'advocates/:username']
    return JsonResponse(data, safe=False)
