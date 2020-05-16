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
                    'partial_update': 'book.change_book'
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