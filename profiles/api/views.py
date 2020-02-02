from rest_framework import generics,permissions
from profiles.models import Profile
from books.models import Book
from .serializers import (
    ProfileListSerializer,
    ProfileDetailSerializer,
    ProfileUpdateSerializer
)
from bookapp_api.permissions import IsOwnerOrReadOnly

class ProfileListAPIView(generics.ListAPIView):
    queryset=Profile.objects.all()
    serializer_class=ProfileListSerializer
    permission_classes=[permissions.AllowAny]

class ProfileDetailAPIView(generics.RetrieveAPIView):
    queryset=Profile.objects.all()
    serializer_class=ProfileDetailSerializer
    permission_classes=[permissions.AllowAny]


class ProfileUpdateAPIView(generics.UpdateAPIView):
    queryset=Profile.objects.all()
    serializer_class=ProfileUpdateSerializer
    permissions=[IsOwnerOrReadOnly]


    def perform_update(self, serializer):
        data=self.request.data
        serializer.save(
            wish=data.get('wish'),
            book=data.get('book'),
            currently=data.get('currently'),
            image=data.get('image'),
            follow=data.get('follow')
        )


