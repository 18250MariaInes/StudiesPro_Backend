from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import datetime
from permissions.services import APIPermissionClassFactory
from exam.models import Exam
from exam.serializers import ExamSerializer
from course.models import Course
from course.serializer import CourseSerializer



def evaluar(user, obj, request):
    return user.name == obj.student.name


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='ExamPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'list': True,
                    #'bulk_happy_birthday': lambda user, req: user.is_authenticated,
                },
                'instance': {
                    'retrieve': 'exam.view_exam',
                    'destroy': 'exam.destroy_exam',
                    'update': True,
                    'partial_update': 'exam.change_exam',
                    'notify': evaluar,
                    'update_title': evaluar,
                    'update_topics': evaluar,
                    'update_date': evaluar,
                    'update_course': evaluar,
                    'delete_exam': evaluar,
                    # 'update_permissions': 'users.add_permissions'
                    # 'archive_all_students': phase_user_belongs_to_school,
                    # 'add_clients': True,
                }
            }
        ),
    )

    def perform_create(self, serializer):
        exam = serializer.save()
        user = self.request.user
        assign_perm('exam.view_exam', user, exam)
        assign_perm('exam.change_exam', user, exam)
        assign_perm('exam.destroy_exam', user, exam)
        return Response(serializer.data)


    @action(detail=True, url_path='update-title', methods=['patch'])
    def update_title(self, request, pk=None):
        exam = self.get_object()

        new_title = request.data.get('new_title')
        exam.title = new_title
        exam.save()

        return Response(ExamSerializer(exam).data)

    @action(detail=True, url_path='update-topics', methods=['patch'])
    def update_topics(self, request, pk=None):
        exam = self.get_object()

        new_topics = request.data.get('new_topics')
        exam.topics = new_topics
        exam.save()

        return Response(ExamSerializer(exam).data)
    
    @action(detail=True, url_path='update-date', methods=['patch'])
    def update_date(self, request, pk=None):
        exam = self.get_object()

        new_date = request.data.get('new_date')
        new_date = datetime.datetime.strptime(new_date, '%Y-%m-%d').date()
        exam.date = new_date
        exam.save()

        return Response(ExamSerializer(exam).data)

    @action(detail=True, url_path='update-course', methods=['patch'])
    def update_course(self, request, pk=None):
        exam = self.get_object()

        new_course = request.data.get('new_course')
        courseNew = Course.objects.get(id=new_course)
        exam.course = courseNew
        exam.save()

        return Response(ExamSerializer(exam).data)
    

    @action(detail=True, url_path='delete_exam', methods=['delete'])
    def delete_exam(self, request, pk=None):
        exam = self.get_object()
        exam.delete()
        print ("Examen eliminado")
