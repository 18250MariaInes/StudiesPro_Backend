from rest_framework import serializers

from teacher.models import Teacher
#from parents.serializer import ParentSerializer

class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = (
            'id',
            'name',
            'lastname',
            'email'
        )