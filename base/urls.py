from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.endpoints),

    path('get_advocate/', views.get_an_advocate),
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh_view'),

    path('advocates/', views.advocate_list, name="advocates"),
    # path('advocates/<str:username>/', views.advocate_detail),
    path('advocates/<str:username>/', views.AdvocateDetail.as_view()),

    path('companies/', views.companies_list)
    #companies/:id
]