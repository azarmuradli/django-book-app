from rest_framework import generics,permissions
from books.models import Book
from .serializers import BookListSerializer,BookDetailSerializer
from rest_framework import filters


class BookListAPIView(generics.ListAPIView):
    queryset=Book.objects.all()
    serializer_class=BookListSerializer
    permission_classes=[permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title','author__user__username']
    list_display = ['title']

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

class BookDetailAPIView(generics.RetrieveAPIView):
    queryset=Book.objects.all()
    serializer_class=BookDetailSerializer
    permission_classes=[permissions.AllowAny]



