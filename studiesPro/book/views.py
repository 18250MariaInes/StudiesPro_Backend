from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions.services import APIPermissionClassFactory
from book.models import Book
from book.serializer import BookSerializer

def evaluate(user, obj, request):
    return user.name == obj.student.name

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='BookPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'list': True,
                },
                'instance': {
                    'retrieve': 'book.view_book',
                    'destroy': False,
                    'update': True,
                    'partial_update': 'book.change_book',
                    'update_title': evaluate,
                    'update_description': evaluate,
                    'update_date': evaluate,
                }
            }
        ),
    )

    def perform_create(self, serializer):
        book = serializer.save()
        user = self.request.user
        assign_perm('book.change_book', user, book)
        assign_perm('book.change_book', user, book)
        return Response(serializer.data)

    @action(detail=True, url_path='update-title', methods=['patch'])
    def update_title(self, request, pk=None):
        book = self.get_object()

        new_title = request.data.get('new_title')
        book.title = new_title
        book.save()

        return Response(BookSerializer(book).data)
    
    @action(detail=True, url_path='update-description', methods=['patch'])
    def update_description(self, request, pk=None):
        book = self.get_object()

        new_description = request.data.get('new_description')
        book.description = new_description
        book.save()

        return Response(BookSerializer(book).data)
    
    @action(detail=True, url_path='update-date', methods=['patch'])
    def update_date(self, request, pk=None):
        book = self.get_object()

        new_date = request.data.get('new_date')
        book.date = new_date
        book.save()

        return Response(BookSerializer(book).data)