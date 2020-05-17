from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import datetime
from permissions.services import APIPermissionClassFactory
from delvas.models import Delvas
from delvas.serializer import DelvasSerializer

def evaluate(user, obj, request):
    return user.name == obj.student.name

class DelvasViewSet(viewsets.ModelViewSet):
    queryset = Delvas.objects.all()
    serializer_class = DelvasSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='DelvasPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'list': True,
                },
                'instance': {
                    'retrieve': 'delvas.view_delvas',
                    'destroy': False,
                    'update': True,
                    'partial_update': 'delvas.change_delvas',
                    'update_name': evaluate,
                    'delete_date': evaluate                    
                }
            }
        ),
    )

    def perform_create(self, serializer):
        delvas = serializer.save()
        user = self.request.user
        assign_perm('delvas.view_delvas', user, delvas)
        assign_perm('delvas.change_delvas', user, delvas)
        return Response(serializer.data)
    
    @action(detail=True, url_path='update-name', methods=['patch'])
    def update_name(self, request, pk=None):
        delvas = self.get_object()

        new_name = request.data.get('new_name')
        delvas.name = new_name
        delvas.save()

        return Response(DelvasSerializer(delvas).data)
    
    @action(detail=True, url_path='update-date', methods=['patch'])
    def update_date(self, request, pk=None):
        delvas = self.get_object()

        new_date = request.data.get('new_date')
        new_date = datetime.datetime.strptime(new_date, '%Y-%m-%d').date()
        delvas.date = new_date
        delvas.save()

        return Response(DelvasSerializer(delvas).data)
