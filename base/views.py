from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Advocate, Company
from .serializers import AdvocateSerializer, CompanySerializer 

# Create your views here.

# don't deploy with sqlite

@api_view(['GET'])
def endpoints(req):
    data = ['/advocates', 'advocates/:username']
    return Response(data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
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

class AdvocateDetail(APIView):
    """
    View the details of each advocate
    """

    def get_object(self, username):
        try:
            return Advocate.objects.get(username=username)
        except Advocate.DoesNotExist:
            return Response('Advocate not found')

    def get(self, req, username):
        advocate = self.get_object(username)
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)
    
    def put(self, req, username):
        advocate = self.get_object(username)
        advocate.username = req.data['username']
        advocate.bio = req.data['bio']

        advocate.save()

        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)
    
    def delete(self, req, username):
        advocate = self.get_object(username)
        advocate.delete()
        return Response('user was deleted')



# @api_view(['GET', 'PUT', 'DELETE'])
# def advocate_detail(req, username):

#     advocate = Advocate.objects.get(username=username)

#     if req.method == 'GET':
#         serializer = AdvocateSerializer(advocate, many=False)
#         return Response(serializer.data)

#     if req.method == 'PUT':
#         advocate.username = req.data['username']
#         advocate.bio = req.data['bio']

#         advocate.save()

#         serializer = AdvocateSerializer(advocate, many=False)
#         return Response(serializer.data)

#     if req.method == 'DELETE':
#         advocate.delete()
#         return Response('user was deleted')

@api_view(['GET'])
def companies_list(req):
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)
