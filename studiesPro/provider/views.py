from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions.services import APIPermissionClassFactory
from provider.models import Provider
from material.models import Material
from provider.serializers import ProviderSerializer
from material.serializers import MaterialSerializer


def evaluar(user, obj, request):
    return user.name == obj.student.name


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='ProviderPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'list': True,
                    #'bulk_happy_birthday': lambda user, req: user.is_authenticated,
                },
                'instance': {
                    'retrieve': 'provider.view_provider',
                    'destroy': 'provider.destroy_provider',
                    'update': evaluar,
                    'partial_update': 'provider.change_provider',
                    'notify': evaluar,
                    'update_name': evaluar,
                    'update_address': evaluar,
                    'update_email': evaluar,
                    'delete_provider': evaluar,
                    'materials':evaluar,
                    # 'update_permissions': 'users.add_permissions'
                    # 'archive_all_students': phase_user_belongs_to_school,
                    # 'add_clients': True,
                }
            }
        ),
    )

    def perform_create(self, serializer):
        provider = serializer.save()
        student = self.request.user
        assign_perm('provider.view_provider', student, provider)
        assign_perm('provider.change_provider', student, provider)
        assign_perm('provider.destroy_provider', student, provider)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def notify(self, request, pk=None):
        provider = self.get_object()

        # TODO: conectarme a FCM y mandar la push
        print("Contacto: ", provider.email)

        return Response({
            'status': 'ok'
        })

    @action(detail=True, url_path='update-name', methods=['patch'])
    def update_name(self, request, pk=None):
        provider = self.get_object()

        new_name = request.data.get('new_name')
        provider.name = new_name
        provider.save()

        return Response(ProviderSerializer(provider).data)

    @action(detail=True, url_path='update-address', methods=['patch'])
    def update_address(self, request, pk=None):
        provider = self.get_object()

        new_address = request.data.get('new_address')
        provider.address = new_address
        provider.save()

        return Response(ProviderSerializer(provider).data)
    
    @action(detail=True, url_path='update-email', methods=['patch'])
    def update_email(self, request, pk=None):
        provider = self.get_object()

        new_email = request.data.get('new_email')
        provider.email = new_email
        provider.save()

        return Response(ProviderSerializer(provider).data)
    

    @action(detail=True, url_path='delete_provider', methods=['delete'])
    def delete_provider(self, request, pk=None):
        provider = self.get_object()
        provider.delete()
        print ("Provider eliminado")
    
    @action(detail=True, methods=['get'])
    def materials(self, request, pk=None):
        provider = self.get_object()
        material_provider = []
        for material in Material.objects.filter(provider=provider):
            material_provider.append(MaterialSerializer(material).data)
        return Response(material_provider)
    
