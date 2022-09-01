from django.core.management.base import BaseCommand
from account.models import *
from review.models import *
from tutoring.models import *
import string, random

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        
        # 5 Random Courses and Students

        students = random.sample(list(Student.objects.all()), 5)
        courses = random.sample(list(Course.objects.all()), 5)
        descriptions = [
            'This class was great',
            'Class was too hard',
            'Very time consuming!',
            'I like pizza',
            'Amazing curve!',
        ]

        for i in students:
            for j in courses:
                review = Review.objects.create(course=j, student=i, description=random.choice(descriptions))

        print('DONE')
