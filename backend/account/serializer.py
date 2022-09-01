from rest_framework import serializers

from .models import Student

# Wouldn't this be a bit too heavy?
class StudentSerializer(serializers.Serializer):
    model = Student
    fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'user_college', 'user_major',
              'user_interest1', 'user_interest2', 'user_interest3', 'current_courses', 'past_courses',
              'tutoring_courses', 'user_karma', 'profile_pic']