from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions.services import APIPermissionClassFactory
from semester.models import Semester 
from course.models import Course 
from semester.serializer import SemesterSerializer 
from course.serializer import CourseSerializer 

def evaluate(user, obj, request):
    return user.name == obj.student.name

class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer 
    permission_classes = (
        APIPermissionClassFactory(
            name='SemesterPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'list': True,
                },
                'instance': {
                    'retrieve': 'semester.view_semester',
                    'destroy': False,
                    'update': True,
                    'partial_update': 'semester.change_semester',
                    'courses':evaluate,
                    'update_beginning':evaluate,
                    'update_end':evaluate
                }
            }
        ),
    )

    def perform_create(self, serializer):
        semester = serializer.save()
        user = self.request.user
        assign_perm('semester.view_semester', user, semester)
        assign_perm('semester.change_semester', user, semester)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def courses(self, request, pk=None):
        semester = self.get_object()
        courses_semester=[]
        for course in Course.objects.filter(semester=semester):
            courses_semester.append(CourseSerializer(course).data)
        return Response(courses_semester)
    
    @action(detail=True, url_path='update-beginning', methods=['patch'])
    def update_beginning(self, request, pk=None):
        semester = self.get_object()

        new_beginning = request.data.get('new_beginning')
        semester.beginning = new_beginning
        semester.save()

        return Response(SemesterSerializer(semester).data)

    @action(detail=True, url_path='update-end', methods=['patch'])
    def update_end(self, request, pk=None):
        semester = self.get_object()

        new_end = request.data.get('new_end')
        semester.end = new_course
        semester.save()

        return Response(SemesterSerializer(semester).data)

