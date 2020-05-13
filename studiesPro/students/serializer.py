from rest_framework import serializers

from students.models import Student
#from parents.serializer import ParentSerializer

class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = (
            'id',
            'name',
            'lastname',
            'carne',
            'sship'
        )