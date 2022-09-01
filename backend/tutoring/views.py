from api.serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from account.models import *
from account.LISTS import *
from .models import *
import json
from rest_framework.parsers import JSONParser



# TESTING ONLY #

class GetCoursesSample(APIView):

    def get(self, request):
        student = Student.objects.get(pk=1)

        queryset1 = student.current_courses.all()
        serializer1 = CourseSerializer(queryset1, many=True)
        data1 = serializer1.data

        queryset2 = student.past_courses.all()
        serializer2 = CourseSerializer(queryset2, many=True)
        data2 = serializer2.data

        queryset3 = student.tutoring_courses.all()
        serializer3 = CourseSerializer(queryset3, many=True)
        data3 = serializer3.data

        return Response({
            'current_courses': data1, 
            'past_courses': data2,
            'tutoring_courses': data3
        })

    def put(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            course_dept, course_num = serializer.data['course_dept'], serializer.data['course_num']
            course = Course.objects.get(course_dept=course_dept, course_num=course_num)
            student = Student.objects.get(pk=1)
            student.tutoring_courses.remove(course)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# END TESTING SECTION #



class GetCurrentCourses(APIView):
    authentication_classes = [TokenAuthentication]

    # Retrieve CURRENT classes 
    def get(self, request):
        if (request.user.is_authenticated):
            student = Student.objects.get(pk=request.user.id)
            queryset = student.current_courses.all()
            serializer = CourseSerializer(queryset, many=True)
            data = serializer.data
            return Response(data)
        return Response({})

    # Put request REMOVES course from CURRENT courses of Student
    def put(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            course_dept, course_num = serializer.data['course_dept'], serializer.data['course_num']
            course = Course.objects.get(course_dept=course_dept, course_num=course_num)
            student = Student.objects.get(pk=1)
            student.tutoring_courses.remove(course)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetPastCourses(APIView):
    authentication_classes = [TokenAuthentication]

    # Retrieve PAST classes 
    def get(self, request):
        if (request.user.is_authenticated):
            student = Student.objects.get(pk=request.user.id)
            queryset = student.past_courses.all()
            serializer = CourseSerializer(queryset, many=True)
            data = serializer.data
            return Response(data)
        return Response({})

    # Put request REMOVES course from PAST courses of Student
    def put(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            course_dept, course_num = serializer.data['course_dept'], serializer.data['course_num']
            course = Course.objects.get(course_dept=course_dept, course_num=course_num)
            student = Student.objects.get(pk=1)
            student.past_courses.remove(course)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetTutoringCourses(APIView):
    authentication_classes = [TokenAuthentication]

    # Retrieve TUTORING classes 
    def get(self, request):
        if (request.user.is_authenticated):
            student = Student.objects.get(pk=request.user.id)
            queryset = student.tutoring_courses.all()
            serializer = CourseSerializer(queryset, many=True)
            data = serializer.data
            return Response(data)
        return Response({})

    # Put request REMOVES course from TUTORING courses of Student
    def put(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            course_dept, course_num = serializer.data['course_dept'], serializer.data['course_num']
            course = Course.objects.get(course_dept=course_dept, course_num=course_num)
            student = Student.objects.get(pk=1)
            student.tutoring_courses.remove(course)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAllCourses(APIView):
    authentication_classes = [TokenAuthentication]

    # Retrieve ALL classes 
    def get(self, request):
        if (request.user.is_authenticated):
            student = Student.objects.get(pk=request.user.id)

            queryset1 = student.current_courses.all()
            serializer1 = CourseSerializer(queryset1, many=True)
            data1 = serializer1.data

            queryset2 = student.past_courses.all()
            serializer2 = CourseSerializer(queryset2, many=True)
            data2 = serializer2.data

            queryset3 = student.tutoring_courses.all()
            serializer3 = CourseSerializer(queryset3, many=True)
            data3 = serializer3.data

            return Response({
                'current_courses': data1, 
                'past_courses': data2,
                'tutoring_courses': data3
            })
        return Response({})

def markComplete(request, pk):
    updated_course = Course.objects.get(id=pk)
    request.user.student.current_courses.remove(updated_course)
    request.user.student.past_courses.add(updated_course)

def markCurrent(request, pk):
    updated_course = Course.objects.get(id=pk)
    request.user.student.past_courses.remove(updated_course)
    request.user.student.current_courses.add(updated_course)

def becomeTutor(request, pk):
    course = Course.objects.get(id=pk)
    request.user.student.past_courses.remove(course)
    request.user.student.tutoring_courses.add(course)

class FindPeer(APIView):

    def get(self, request, pk1, pk2):
        course = Course.objects.get(course_dept=pk1, course_num=pk2)
        queryset = Student.objects.filter(current_courses__in=[course])
        serializer = StudentSerializer(queryset, many=True)
        data = serializer.data
        return Response(data)


class FindTutor(APIView):

    def get(self, request, pk1, pk2):
        course = Course.objects.get(course_dept=pk1, course_num=pk2)
        queryset = Student.objects.filter(tutoring_courses__in=[course])
        serializer = StudentSerializer(queryset, many=True)
        data = serializer.data
        return Response(data)


