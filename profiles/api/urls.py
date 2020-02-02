from django.contrib import admin
from django.urls import path
from .views import (
    ProfileListAPIView,
    ProfileDetailAPIView,
    ProfileUpdateAPIView
)

urlpatterns = [
    path('',ProfileListAPIView.as_view(),name='list'),
    path('<int:pk>/',ProfileDetailAPIView.as_view(),name='detail'),
    path('<int:pk>/update/',ProfileUpdateAPIView.as_view(),name='update'),
    
]
