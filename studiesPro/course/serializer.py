from rest_framework import serializers

from course.models import Course
from teacher.serializer import TeacherSerializer
from semester.serializer import SemesterSerializer
from students.serializer import StudentSerializer

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = (
            'id',
            'name',
            'teacher',
            'semester',
            'student'
        )