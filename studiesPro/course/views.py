from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions.services import APIPermissionClassFactory
from course.models import Course
from exam.models import Exam
from assignment.models import Assignment
from course.serializer import CourseSerializer
from exam.serializers import ExamSerializer
from assignment.serializers import AssignmentSerializer

def evaluate(user, obj, request):
    return user.name == obj.student.name

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='CoursePermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'list': True,
                },
                'instance': {
                    'retrieve': 'course.view_course',
                    'destroy': False,
                    'update': True,
                    'partial_update': 'course.change_course',
                    'exams':evaluate,
                    'assignments':evaluate,
                    'update_name': evaluate
                }
            }
        ),
    )

    def perform_create(self, serializer):
        course = serializer.save()
        user = self.request.user
        assign_perm('course.view_course', user, course)
        assign_perm('course.change_course', user, course)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def exams(self, request, pk=None):
        course = self.get_object()
        exams_course=[]
        for exam in Exam.objects.filter(course=course):
             exams_course.append(ExamSerializer(exam).data)
        return Response(exams_course)

    @action(detail=True, methods=['get'])
    def assignments(self, request, pk=None):
        course = self.get_object()
        assignments_course=[]
        for assign in Assignment.objects.filter(course=course):
             assignments_course.append(AssignmentSerializer(assign).data)
        return Response(assignments_course)
    
    @action(detail=True, url_path='update-name', methods=['patch'])
    def update_name(self, request, pk=None):
        course = self.get_object()

        new_name = request.data.get('new_name')
        course.name = new_name
        course.save()

        return Response(CourseSerializer(course).data)
    
    
