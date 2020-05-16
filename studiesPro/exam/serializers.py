from rest_framework import serializers
from datetime import date

from exam.models import Exam
from students.serializer import StudentSerializer
from course.serializer import CourseSerializer


class ExamSerializer(serializers.ModelSerializer):
    is_near = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = (
            'id',
            'title',
            'topics',
            'date',
            'student',
            'course',
            'is_near'
        )

    def get_is_near(self, obj):
        d = obj.date
        today = date.today()
        r = (d-today).days
        return r < 3