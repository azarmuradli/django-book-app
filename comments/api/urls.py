from django.contrib import admin
from django.urls import path
from .views import CommentDetailAPIView,CommentListAPIView,CommentCreateAPIView

urlpatterns = [
    path('',CommentListAPIView.as_view(),name='list'),
    path('create/',CommentCreateAPIView.as_view(),name='create'),
    path('<int:pk>/',CommentDetailAPIView.as_view(),name='detail'),
]
