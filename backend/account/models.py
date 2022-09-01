from django.db import models
from django.contrib.auth.models import User
from tutoring.models import Course


# Create your models here.

# 地図: Add fields to Student model
class Student(models.Model):
    COLLEGE_LIST = (
        ('Revelle', 'Revelle'),
        ('Muir', 'Muir'),
        ('Marshall', 'Marshall'),
        ('Warren', 'Warren'),
        ('ERC', 'ERC'),
        ('Sixth', 'Sixth'),
        ('Seventh', 'Seventh'),
    )

    # TODO: Scrape from UCSD website. More comprehensive list of majors.
    MAJOR_LIST = (('Math', 'Mathematics'), ('CS', 'Computer Science'),
                  ('Bio', 'Biology'), ('Japn', 'Japanese Studies'),
                  ('Chem', 'Chemistry'), ('SE', 'Structural Engineering'),
                  ('Phys', 'Physics'), ('EE', 'Electrical Engineering'),
                  ('Poli', 'Political Science')
                  )

    INTEREST_LIST = [('Anime', 'Anime'), ('WoW', 'World of Warcraft'), ('Racoon', 'Racoon Watching'),
                     ('Speeding', 'Driving over speed limit'), ('HW', 'Doing Problem Set'), ('Travel', 'Traveling'),
                     ('CS', 'Counter Strike'), ('LoL', 'League of Legends'), ('Football', 'Football')
                     ]

    student_user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    # Basic user information
    # Changed the naming here so it matches the auth_user to reduce confusion
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    user_college = models.CharField(max_length=200, choices=COLLEGE_LIST, default='')
    user_major = models.CharField(max_length=200, choices=MAJOR_LIST)

    profile_pic = models.ImageField(upload_to='icons',blank=True, default="")

    # User contact info
    phone = models.CharField(max_length=200, default="")
    email = models.CharField(max_length=200, default="")
    ig = models.CharField(max_length=200, default="")
    discord = models.CharField(max_length=200, default="")

    # User interests
    user_interest1 = models.CharField(max_length=200)
    user_interest2 = models.CharField(max_length=200)
    user_interest3 = models.CharField(max_length=200)

    # Do we pre-calculate user attribute?

    # 3 categories of user's classes
    current_courses = models.ManyToManyField(Course, related_name='current_courses_set', blank=True)
    past_courses = models.ManyToManyField(Course, related_name='past_courses_set', blank=True)
    tutoring_courses = models.ManyToManyField(Course, related_name='tutoring_courses_set', blank=True)

    user_karma = models.IntegerField(default=0)

    # I had to change names from fname and lname
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    # 地図: Def for changing setting fields
    def set_karma(self, add_karma):
        # print("！！\nset_karma has been called\n")

        print("self.user_karma before:")
        print(self.user_karma)

        self.user_karma += add_karma
        print("self.user_karma after:")
        print(self.user_karma)

        # print("！！\n")

    def set_college(self, college):
        self.user_college = college

    def set_major(self, major):
        self.user_major = major

    def set_phone(self, phone):
        self.phone = phone

    def set_ig(self, ig):
        self.ig = ig

    def set_discord(self, discord):
        self.discord = discord

    def set_user_interest1(self, user_interest1):
        self.user_interest1 = user_interest1

    def set_user_interest2(self, user_interest2):
        self.user_interest2 = user_interest2

    def set_user_interest3(self, user_interest3):
        self.user_interest3 = user_interest3

    def pack_interests(self):
        return [self.user_interest1, self.user_interest2, self.user_interest3]