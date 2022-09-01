from django.db import models
from account.LISTS import *

# Create your models here.

class Course(models.Model):

    course_dept = models.CharField(max_length=10)
    course_num = models.CharField(max_length=200, null=True)
    prof = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.course_dept} {self.course_num}'