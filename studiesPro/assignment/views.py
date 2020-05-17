from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

import datetime

from permissions.services import APIPermissionClassFactory
from assignment.models import Assignment
from assignment.serializers import AssignmentSerializer
from students.models import Student 
from course.models import Course
from students.serializer import StudentSerializer
from course.serializer import CourseSerializer


def evaluar(user, obj, request):
    return user.name == obj.student.name


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='AssignmentPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'list': True,
                    #'bulk_happy_birthday': lambda user, req: user.is_authenticated,
                },
                'instance': {
                    'retrieve': 'assignment.view_assignment',
                    'destroy': 'assignment.destroy_assignment',
                    'update': True,
                    'partial_update': 'assignment.change_assignment',
                    'notify': evaluar,
                    'update_title': evaluar,
                    'update_description': evaluar,
                    'update_deadline': evaluar,
                    'update_course': evaluar,
                    'delete_assignment': evaluar,
                    # 'update_permissions': 'users.add_permissions'
                    # 'archive_all_students': phase_user_belongs_to_school,
                    # 'add_clients': True,
                }
            }
        ),
    )

    def perform_create(self, serializer):
        assignment = serializer.save()
        user = self.request.user
        assign_perm('assignment.view_assignment', user, assignment)
        assign_perm('assignment.change_assignment', user, assignment)
        assign_perm('assignment.destroy_assignment', user, assignment)
        return Response(serializer.data)


    @action(detail=True, url_path='update-title', methods=['patch'])
    def update_title(self, request, pk=None):
        assignment = self.get_object()

        new_title = request.data.get('new_title')
        assignment.title = new_title
        assignment.save()

        return Response(AssignmentSerializer(assignment).data)

    @action(detail=True, url_path='update-description', methods=['patch'])
    def update_description(self, request, pk=None):
        assignment = self.get_object()

        new_desc = request.data.get('new_desc')
        assignment.description = new_desc
        assignment.save()

        return Response(AssignmentSerializer(assignment).data)
    
    @action(detail=True, url_path='update-deadline', methods=['patch'])
    def update_deadline(self, request, pk=None):
        assignment = self.get_object()

        new_deadline = request.data.get('new_deadline')
        new_deadline = datetime.datetime.strptime(new_deadline, '%Y-%m-%d').date()
        assignment.deadline = new_deadline

        assignment.save()

        return Response(AssignmentSerializer(assignment).data)

    @action(detail=True, url_path='update-course', methods=['patch'])
    def update_course(self, request, pk=None):
        assignment = self.get_object()
        new_course = request.data.get('new_course')
        courseNew = Course.objects.get(id=new_course)
        assignment.course = courseNew
        assignment.save()

        return Response(AssignmentSerializer(assignment).data)
    

    @action(detail=True, url_path='delete_assignment', methods=['delete'])
    def delete_assignment(self, request, pk=None):
        assignment = self.get_object()
        assignment.delete()
        print ("Tarea eliminada")

