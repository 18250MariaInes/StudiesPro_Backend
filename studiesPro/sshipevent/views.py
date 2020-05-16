from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions.services import APIPermissionClassFactory
from sshipevent.models import Sshipevent
from sshipevent.serializers import SshipeventSerializer



def evaluar(user, obj, request):
    return user.name == obj.student.name


class SshipeventViewSet(viewsets.ModelViewSet):
    queryset = Sshipevent.objects.all()
    serializer_class = SshipeventSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='SshipeventPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'list': True,
                    #'bulk_happy_birthday': lambda user, req: user.is_authenticated,
                },
                'instance': {
                    'retrieve': 'sshipevent.view_sshipevent',
                    'destroy': 'sshipevent.destroy_sshipevent',
                    'update': True,
                    'partial_update': 'sshipevent.change_sshipevent',
                    'notify': evaluar,
                    'update_name': evaluar,
                    'update_description': evaluar,
                    'update_hours': evaluar,
                    'update_date': evaluar,
                    'delete_sshipevent': evaluar,
                    # 'update_permissions': 'users.add_permissions'
                    # 'archive_all_students': phase_user_belongs_to_school,
                    # 'add_clients': True,
                }
            }
        ),
    )

    def perform_create(self, serializer):
        sshipevent = serializer.save()
        student = self.request.user
        assign_perm('sshipevent.view_sshipevent', student, sshipevent)
        assign_perm('sshipevent.change_sshipevent', student, sshipevent)
        assign_perm('sshipevent.destroy_sshipevent', student, sshipevent)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def notify(self, request, pk=None):
        sshipevent = self.get_object()

        # TODO: conectarme a FCM y mandar la push
        print("Cantidad de horas realizadas: ", sshipevent.hours)

        return Response({
            'status': 'ok'
        })

    @action(detail=True, url_path='update-name', methods=['patch'])
    def update_name(self, request, pk=None):
        sshipevent = self.get_object()

        new_name = request.data.get('new_name')
        sshipevent.name = new_name
        sshipevent.save()

        return Response(SshipeventSerializer(sshipevent).data)

    @action(detail=True, url_path='update-description', methods=['patch'])
    def update_description(self, request, pk=None):
        sshipevent = self.get_object()

        new_desc = request.data.get('new_desc')
        sshipevent.description = new_desc
        sshipevent.save()

        return Response(SshipeventSerializer(sshipevent).data)
    
    @action(detail=True, url_path='update-hours', methods=['patch'])
    def update_hours(self, request, pk=None):
        sshipevent = self.get_object()

        new_hours = request.data.get('new_hours')
        sshipevent.hours = new_hours
        sshipevent.save()

        return Response(SshipeventSerializer(sshipevent).data)

    @action(detail=True, url_path='update-date', methods=['patch'])
    def update_date(self, request, pk=None):
        sshipevent = self.get_object()

        new_date = request.data.get('new_date')
        sshipevent.date = new_date
        sshipevent.save()

        return Response(SshipeventSerializer(sshipevent).data)
    

    @action(detail=True, url_path='delete_sshipevent', methods=['delete'])
    def delete_sshipevent(self, request, pk=None):
        sshipevent = self.get_object()
        sshipevent.delete()
        print ("Evento de horas beca eliminado")

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