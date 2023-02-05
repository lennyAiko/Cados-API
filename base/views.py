from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def endpoints(req):
    data = ['/advocates', 'advocates/:username']
    return JsonResponse(data, safe=False)

def advocate_list(req):
    data = ['Dennis', 'Lennox', 'Max', 'Tadas']
    return JsonResponse(data, self=False)

def advocate_detail(req, username):
    data = username
    return JsonResponse(data, self=False)