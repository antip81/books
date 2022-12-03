from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from rest_framework.filters import OrderingFilter

from store.models import Book
from store.permissions import IsOwnerOrStaffOrReadOnly
from store.serializers import BooksSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, OrderingFilter]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filterset_fields = ['price']
    search_fields = ['author_name', 'name']
    ordering_fields = ["price", "author_name"]

    def perform_create(self, serializer):
        serializer.validated_data["owner"] = self.request.user
        serializer.save()

def auth(request):
    return render(request, "oauth.html")
