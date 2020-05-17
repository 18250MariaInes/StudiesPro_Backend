from django.shortcuts import render

from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions.services import APIPermissionClassFactory
from teacher.models import Teacher 
from course.models import Course
from teacher.serializer import TeacherSerializer
from course.serializer import CourseSerializer

def evaluate(user, obj, request):
    return user.name == obj.student.name

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='TeacherPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'list': True,
                },
                'instance': {
                    'retrieve': 'teacher.view_teacher',
                    'destroy': evaluate,
                    'update': True,
                    'partial_update': 'teacher.change_teacher',
                    'courses':evaluate,
                    'update_name':evaluate,
                    'update_lastname':evaluate,
                    'update_email':evaluate
                }
            }
        ),
    )

    def perform_create(self, serializer):
        teacher = serializer.save()
        user = self.request.user
        assign_perm('teacher.view_teacher', user, teacher)
        assign_perm('teacher.change_teacher', user, teacher)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def courses(self, request, pk=None):
        teacher = self.get_object()
        courses_teacher=[]
        for course in Course.objects.filter(teacher=teacher):
            courses_teacher.append(CourseSerializer(course).data)
        return Response(courses_teacher)
    
    @action(detail=True, url_path='update-name', methods=['patch'])
    def update_name(self, request, pk=None):
        teacher = self.get_object()

        new_name = request.data.get('new_name')
        teacher.name = new_name
        teacher.save()

        return Response(TeacherSerializer(teacher).data)

    @action(detail=True, url_path='update-lastname', methods=['patch'])
    def update_lastname(self, request, pk=None):
        teacher = self.get_object()

        new_lastname = request.data.get('new_lastname')
        teacher.lastname = new_lastname
        teacher.save()

        return Response(TeacherSerializer(teacher).data)
    
    @action(detail=True, url_path='update-email', methods=['patch'])
    def update_email(self, request, pk=None):
        teacher = self.get_object()

        new_email = request.data.get('new_email')
        teacher.email = new_email
        teacher.save()

        return Response(TeacherSerializer(teacher).data)