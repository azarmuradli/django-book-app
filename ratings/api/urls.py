from django.contrib import admin
from django.urls import path
from .views import RatingCreateAPIView

urlpatterns = [
    path('create/',RatingCreateAPIView.as_view(),name='create'),
    
]
