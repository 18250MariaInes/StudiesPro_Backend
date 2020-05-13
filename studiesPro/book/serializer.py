from rest_framework import serializers

from book.models import Book
from students.serializer import StudentSerializer

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = (
            'id',
            'title',
            'date',
            'student'
        )