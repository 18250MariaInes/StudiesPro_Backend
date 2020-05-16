"""studiesPro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token
)

from assignment.views import AssignmentViewSet
from book.views import BookViewSet
from course.views import CourseViewSet
from delvas.views import DelvasViewSet
from exam.views import ExamViewSet
from material.views import MaterialViewSet
from provider.views import ProviderViewSet
from semester.views import SemesterViewSet
from sshipevent.views import SshipmentViewSet
from students.views import StudentViewSet
from teacher.views import TeacherViewSet


router = routers.DefaultRouter()

router.register(r'assignment', AssignmentViewSet)
router.register(r'book', BookViewSet)
router.register(r'course', CourseViewSet)
router.register(r'delvas', DelvasViewSet)
router.register(r'exam', ExamViewSet)
router.register(r'material', MaterialViewSet)
router.register(r'provider', ProviderViewSet)
router.register(r'semester', SemesterViewSet)
router.register(r'sshipevent', SshipmentViewSet)
router.register(r'students', StudentViewSet)
router.register(r'teacher', TeacherViewSet)


urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/token-auth/', obtain_jwt_token),
    url(r'^api/v1/token-refresh/', refresh_jwt_token),

]
