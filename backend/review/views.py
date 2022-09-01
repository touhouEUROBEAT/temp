from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from account.models import *
from .models import *
from api.serializers import *

# Create your views here.

class GetReviews(APIView):

    def get(self, request, pk1, pk2):
        if (request.user.is_authenticated):
            course = Course.objects.get(course_dept=pk1, course_num=pk2)
            queryset = course.review_set.all()
            serializer = ReviewSerializer(queryset, many=True)
            data = serializer.data
            return Response(data)

