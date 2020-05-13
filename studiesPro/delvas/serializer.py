from rest_framework import serializers

from delvas.models import Delvas
from students.serializer import StudentSerializer

class DelvasSerializer(serializers.ModelSerializer):

    class Meta:
        model = Delvas
        fields = (
            'id',
            'name',
            'date',
            'student'
        )