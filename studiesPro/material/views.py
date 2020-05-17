from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions.services import APIPermissionClassFactory
from material.models import Material
from material.serializers import MaterialSerializer



def evaluar(user, obj, request):
    return user.name == obj.student.name


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='MaterialPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'list': True,
                    #'bulk_happy_birthday': lambda user, req: user.is_authenticated,
                },
                'instance': {
                    'retrieve': 'material.view_material',
                    'destroy': 'material.destroy_material',
                    'update': True,
                    'partial_update': 'material.change_material',
                    'notify': evaluar,
                    'update_name': evaluar,
                    'update_price': evaluar,
                    'update_provider': evaluar,
                    'update_description': evaluar,
                    'delete_material': evaluar,
                    # 'update_permissions': 'users.add_permissions'
                    # 'archive_all_students': phase_user_belongs_to_school,
                    # 'add_clients': True,
                }
            }
        ),
    )

    def perform_create(self, serializer):
        material = serializer.save()
        student = self.request.user
        assign_perm('material.view_material', student, material)
        assign_perm('material.change_material', student, material)
        assign_perm('material.destroy_material', student, material)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def notify(self, request, pk=None):
        material = self.get_object()

        # TODO: conectarme a FCM y mandar la push
        print("Material registrado: ", material.name)

        return Response({
            'status': 'ok'
        })

    @action(detail=True, url_path='update-name', methods=['patch'])
    def update_name(self, request, pk=None):
        material = self.get_object()

        new_name = request.data.get('new_name')
        material.name = new_name
        material.save()

        return Response(MaterialSerializer(material).data)

    @action(detail=True, url_path='update-price', methods=['patch'])
    def update_price(self, request, pk=None):
        material = self.get_object()

        new_price = request.data.get('new_price')
        material.price = new_price
        material.save()

        return Response(MaterialSerializer(material).data)

    @action(detail=True, url_path='update-description', methods=['patch'])
    def update_description(self, request, pk=None):
        material = self.get_object()

        new_description = request.data.get('new_description')
        material.description = new_description
        material.save()

        return Response(MaterialSerializer(material).data)
    

    @action(detail=True, url_path='delete_material', methods=['delete'])
    def delete_material(self, request, pk=None):
        material = self.get_object()
        material.delete()
        print ("materialen eliminado")
