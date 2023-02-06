from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q

from .models import Advocate
from .serializers import AdvocateSerializer

# Create your views here.

# don't deploy with sqlite

@api_view(['GET'])
def endpoints(req):
    data = ['/advocates', 'advocates/:username']
    return Response(data)

@api_view(['GET', 'POST'])
def advocate_list(req):
    # Handles GET requests
    #/advocates/?query=#
    if req.method == 'GET':
        query = req.GET.get('query')

        if query == None:
            query = ''

        #contains prevents searching for an exact match
        advocates = Advocate.objects.filter(
            Q(username__icontains=query) | Q(bio__icontains=query)
            )
        serializer = AdvocateSerializer(advocates, many=True)
        return Response(serializer.data)
    
    if req.method == 'POST':
        advocate = Advocate.objects.create(
            username=req.data['username'],
            bio=req.data['bio']
        )

        serializer = AdvocateSerializer(advocate, many=False)

        return Response(serializer.data)


@api_view(['GET'])
def advocate_detail(req, username):
    advocate = Advocate.objects.get(username=username)
    serializer = AdvocateSerializer(advocate, many=False)
    return Response(serializer.data)