from rest_framework import serializers
from datetime import date
from book.models import Book
from students.serializer import StudentSerializer

class BookSerializer(serializers.ModelSerializer):
    is_near = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = (
            'id',
            'title',
            'description',
            'date',
            'student',
            'is_near'
        )

    def get_is_near(self, obj):
        d = obj.date
        today = date.today()
        r = (d-today).days
        return r < 3