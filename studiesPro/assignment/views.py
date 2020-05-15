from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions.services import APIPermissionClassFactory
from assignment.models import Assignment
from assignment.serializers import AssignmentSerializer



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
        student = self.request.user
        assign_perm('assignment.view_assignment', student, assignment)
        assign_perm('assignment.change_assignment', student, assignment)
        assign_perm('assignment.destroy_assignment', student, assignment)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def notify(self, request, pk=None):
        assignment = self.get_object()

        # TODO: conectarme a FCM y mandar la push
        print("Responsable: ", assignment.student.name)

        return Response({
            'status': 'ok'
        })

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
        assignment.deadline = new_deadline
        assignment.save()

        return Response(AssignmentSerializer(assignment).data)

    @action(detail=True, url_path='update-course', methods=['patch'])
    def update_course(self, request, pk=None):
        assignment = self.get_object()

        new_course = request.data.get('new_course')
        assignment.course = new_course
        assignment.save()

        return Response(AssignmentSerializer(assignment).data)
    

    @action(detail=True, url_path='delete_assignment', methods=['delete'])
    def delete_assignment(self, request, pk=None):
        assignment = self.get_object()
        assignment.delete()
        print ("Tarea eliminada")

    #@action(detail=True, url_path='happy-bday', methods=['post'])
    #def happy_birthday(self, request, pk=None):
    #    assignment = self.get_object()
    #    self.increment_age(pet)
    #    print ("Happy birthday {}!".format(pet.name))
    #    return Response(PetSerializer(pet).data)
    

    #@action(detail=False, url_path='happy-bday', methods=['post'])
    #def bulk_happy_birthday(self, request):
    #    for pet in Pet.objects.all():
    #        # TODO: send push
    #        self.increment_age(pet)
    #
    #    return Response({})

    #def increment_age(self, pet):
    #    pet.age += 1
    #    pet.save()
    #    print ("Happy birthday {}!".format(pet.name))
