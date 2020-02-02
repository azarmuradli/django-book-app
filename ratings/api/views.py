from rest_framework import generics,permissions
from ratings.models import Rating
from .serializers import RatingCreateSerializer

class RatingCreateAPIView(generics.CreateAPIView):
    queryset=Rating.objects.all()
    serializer_class=RatingCreateSerializer
    permission_classes=[permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.set_profile)