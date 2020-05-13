from rest_framework import serializers

from semester.models import Semester
#from parents.serializer import ParentSerializer

class SemesterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Semester
        fields = (
            'id',
            'beginning',
            'end'
        )