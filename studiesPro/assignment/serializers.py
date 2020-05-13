from rest_framework import serializers
from datetime import date

from assignment.models import Assignment
from students.serializers import StudentSerializer
from course.serializers import CourseSerializer


class AssignmentSerializer(serializers.ModelSerializer):
    is_near = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = (
            'id',
            'title',
            'description',
            'deadline',
            'student',
            'course',
            'is_near'
        )

    def get_is_near(self, obj):
        d = obj.deadline
        today = date.today()
        r = (d-today).days
        return r < 3