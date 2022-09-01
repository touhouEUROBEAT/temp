from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from .serializers import *
from account.models import Student
from tutoring.models import Course

class CurrentCourseView(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    def get_queryset(self):
        student = self.request.user.student
        return student.current_courses.all()

class CompletedCourseView(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    def get_queryset(self):
        student = self.request.user.student
        return student.past_courses.all()

class TutoringCourseView(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    def get_queryset(self):
        student = self.request.user.student
        return student.tutoring_courses.all()