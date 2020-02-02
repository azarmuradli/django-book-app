from django.contrib import admin
from django.urls import path
from .views import BookListAPIView,BookDetailAPIView

urlpatterns = [
    path('',BookListAPIView.as_view(),name='list'),
    path('<int:pk>',BookDetailAPIView.as_view(),name='detail')
]
