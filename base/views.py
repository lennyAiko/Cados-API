from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
import requests
import random

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Advocate, Company
from .serializers import AdvocateSerializer, CompanySerializer 

# Create your views here.

COMPANIES = ['stack overflow', 'mongodb', 'agora', 'github', 'meta', 'facebook', 'whatsapp', 'twitter', 'doodads']

def fetcher(page):
    url = f'https://cados.up.railway.app/advocates/?query=&page={page}'
    res = requests.get(url).json()
    return res['advocates']

def check_if_exist(user, advocates):
    if user['username'] in advocates: 
        return True
    return False

def create_objects(company, data):
    store.append(data['username'])
    company_object = Company.objects.create(
                name = company,
                bio = 'Lorem Ipsum'
    )
    Advocate.objects.create(
        username = data['username'],
        name = data['name'],
        bio = data['bio'],
        twitter = data['twitter'],
        profile_pic = data['profile_pic'],
        company = company_object
    )
    company_object.save()
    

value = []
pages = []
store = []

@api_view(['GET'])
def get_an_advocate(req):
    
    count = len(value)
    page = len(pages) + 1
    company = COMPANIES[random.randint(0, len(COMPANIES)-1)]

    data = fetcher(page)

    count += 1
    value.append(count)
    if count == 20:
        value.clear()
        print(count)
        page += 1
        pages.append(page)

    data = data[count-1]

    if len(store) > 0:

        check = check_if_exist(data, store)
        if check is False:
            create_objects(company, data)
            return Response('A new advocate added!') 
        if check is True: 
            count += 1
            return Response('Already exist!')
    else:
        create_objects(company, data)
        return Response('A new advocate added here!')

@api_view(['GET'])
def endpoints(req):
    data = ['/advocates', 'advocates/:username']
    return Response(data)


# @permission_classes([IsAuthenticated])
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
            Q(username__icontains=query) | Q(bio__icontains=query) | Q(name__icontains=query)
            )
        serializer = AdvocateSerializer(advocates, many=True)

        total_advocates = Advocate.objects.all().count()
        total_query_advocates = advocates.count()
        return Response({"advocates": serializer.data, "total": total_advocates, "query": total_query_advocates})
    
    if req.method == 'POST':
        advocate = Advocate.objects.create(
            username=req.data['username'],
            bio=req.data['bio']
        )

        serializer = AdvocateSerializer(advocate, many=False)

        return Response(serializer.data)

# @api_view(['GET'])
# def advocate_detail(req, username):
#     try:
#         advocate = Advocate.objects.get(username=username)
#     except Advocate.DoesNotExist:
#         return Response('Advocate not found')

#     print(username)
#     serializer = AdvocateSerializer(advocate, many=False)
#     return Response(serializer.data)


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
