from rest_framework import generics
from likes.models import Like
from .serializers import LikeCreateSerializer

class LikeCreateAPIView(generics.CreateAPIView):
    queryset=Like.objects.all()
    serializer_class=LikeCreateSerializer
    