from django.db import models
from tutoring.models import Course
from account.models import Student
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Review(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    rating = models.IntegerField(
        default=5,
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    description = models.TextField()