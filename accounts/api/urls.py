from django.urls import path,include
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token
from .views import LoginAPIView,RegisterAPIView,UserUpdateAPIView

urlpatterns = [
    path('login/',LoginAPIView.as_view(),name='login'),
    path('register/',RegisterAPIView.as_view(),name='register'),
    path('<int:pk>/update',UserUpdateAPIView.as_view(),name='update'),
    path('jwt',obtain_jwt_token),
    path('jwt/refresh/',refresh_jwt_token),
]