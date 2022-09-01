from django.core.management.base import BaseCommand
from account.models import *
import string, random
from account.LISTS import *

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        
        # Populate database with 10 Courses

        a = [i for i in range(1, 100)]
        
        cd = random.choices(DEPT_LIST, k=10)
        
        cn = random.choices(a, k=10)
        
        for i in range(10):
            c =  Course(course_dept = cd[i][0], course_num = cn[i])
            c.save()

        #auth_user(u_id 1 - 26)

        usernames = string.ascii_lowercase
        pword = "abc"
        
        firstnames = ['Alice', 'Bob', 'Eve', 'Trent', 'Mallory', 'John', 'Tan', 'Caleb',
            'Andrew', 'Emily', 'Evelyn', 'Jiting', 'Keystone', 'Corona', 'BudLight',
            'Kirin', 'Sapporo', 'Ebisu', 'Shifu', 'Tigress', 'Mantis', 'PandaHimself', 'Monkey',
            'Crane', 'Viper', 'Oogway']
        lastnames = string.ascii_lowercase
          
        added_courses = list(Course.objects.all())

        for i in range(26):

            # Create User
            tempUser = User.objects.create_user(username=usernames[i], password=pword)
            tempUser.email = usernames[i] + "@ucsd.edu"
            tempUser.first_name = firstnames[i]
            tempUser.last_name = lastnames[i]

            tempUser.save()

            # Create Student
            tempStudent = Student(pk = tempUser.id, student_user=tempUser)
            tempStudent.fname = firstnames[i]
            tempStudent.lname = lastnames[i]
            tempStudent.user_college = random.choice(COLLEGE_LIST)[0]
            tempStudent.user_major = random.choice(MAJOR_LIST)[0]
            tempStudent.email = usernames[i] + "@ucsd.edu"
            

            interests = random.choices(INTEREST_LIST, k=3)
        
            tempStudent.user_interest1 = interests[0][0]
            tempStudent.user_interest2 = interests[1][0]
            tempStudent.user_interest3 = interests[2][0]
        
            tempStudent.save()
        
            courses = random.choices(added_courses, k=3)
            for j in courses:
                tempStudent.current_courses.add(j)
        
            tempStudent.save()

        print('DONE')
