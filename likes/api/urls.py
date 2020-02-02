from django.contrib import admin
from django.urls import path
from .views import LikeCreateAPIView

urlpatterns = [
    path('create/',LikeCreateAPIView.as_view(),name='create'),
    
]
