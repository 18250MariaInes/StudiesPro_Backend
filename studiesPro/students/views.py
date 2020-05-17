from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions.services import APIPermissionClassFactory
from students.models import Student 
from course.models import Course 
from sshipevent.models import Sshipevent 
from delvas.models import Delvas 
from book.models import Book 
from material.models import Material
from exam.models import Exam 
from assignment.models import Assignment 
from teacher.models import Teacher
from provider.models import Provider

from students.serializer import StudentSerializer
from course.serializer import CourseSerializer 
from sshipevent.serializers import SshipeventSerializer 
from delvas.serializer import DelvasSerializer 
from book.serializer import BookSerializer 
from material.serializers import MaterialSerializer
from exam.serializers import ExamSerializer 
from assignment.serializers import AssignmentSerializer 
from teacher.serializer import TeacherSerializer
from provider.serializers import ProviderSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset= Student.objects.all()
    serializer_class=StudentSerializer

    @action(detail=True, methods=['get'])
    def courses(self, request, pk=None):
        student = self.get_object()
        course_user = []
        for course in Course.objects.filter(student=student):
            course_user.append(CourseSerializer(course).data)
        return Response(course_user)

    @action(detail=True, methods=['get'])
    def sshipevents(self, request, pk=None):
        student = self.get_object()
        sshipevents_user = []
        for sshipevent in Sshipevent.objects.filter(student=student):
            sshipevents_user.append(SshipeventSerializer(sshipevent).data)
        return Response(sshipevents_user)

    @action(detail=True, methods=['get'])
    def delvas(self, request, pk=None):
        student = self.get_object()
        delvas_user = []
        for delvas in Delvas.objects.filter(student=student):
            delvas_user.append(DelvasSerializer(delvas).data)
        return Response(delvas_user)

    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        student = self.get_object()
        books_user = []
        for book in Book.objects.filter(student=student):
            books_user.append(BookSerializer(book).data)
        return Response(books_user)
    
    @action(detail=True, methods=['get'])
    def materials(self, request, pk=None):
        student = self.get_object()
        materials_user = []
        for material in Material.objects.filter(student=student):
            materials_user.append(MaterialSerializer(material).data)
        return Response(materials_user)
    
    @action(detail=True, methods=['get'])
    def exams(self, request, pk=None):
        student = self.get_object()
        exams_user = []
        for exam in Exam.objects.filter(student=student):
            exams_user.append(ExamSerializer(exam).data)
        return Response(exams_user)

    @action(detail=True, methods=['get'])
    def assignments(self, request, pk=None):
        student = self.get_object()
        assignments_user = []
        for assignment in Assignment.objects.filter(student=student):
            assignments_user.append(AssignmentSerializer(assignment).data)
        return Response(assignments_user)

    @action(detail=True, methods=['get'])
    def teachers(self, request, pk=None):
        student = self.get_object()
        course_user = []
        teacher_course_user = []
        for course in Course.objects.filter(student=student):
            #print(CourseSerializer(course).data["teacher"])
            t=Teacher.objects.get(id=CourseSerializer(course).data["teacher"])
            #print (t)
            for teacher in Teacher.objects.filter(name=t):
                #print(TeacherSerializer(teacher).data)
                teacher_course_user.append(TeacherSerializer(teacher).data) 
        return Response(teacher_course_user)
    
    @action(detail=True, methods=['get'])
    def providers(self, request, pk=None):
        student = self.get_object()
        provider_material_user = []
        for material in Material.objects.filter(student=student):
            p=Provider.objects.get(id=MaterialSerializer(material).data["provider"])
            for provider in Provider.objects.filter(name=p):
                provider_material_user.append(ProviderSerializer(provider).data)
        return Response(provider_material_user) 

        


 
