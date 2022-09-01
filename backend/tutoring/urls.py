from django.urls import path
from . import views

urlpatterns=[
    # For testing purposes
    path('get_courses_sample/', views.GetCoursesSample.as_view(), name='get_courses_sample'),

    # Main URL to retrieve all courses
    path('get_all_courses/', views.GetAllCourses.as_view(), name='get_all_courses'),

    # Use put requests to remove courses
    path('get_current_courses/', views.GetCurrentCourses.as_view(), name='get_current_courses'),
    path('get_past_courses/', views.GetPastCourses.as_view(), name='get_past_courses'),
    path('get_tutoring_courses/', views.GetTutoringCourses.as_view(), name='get_tutoring_courses'),


    path('mark_complete/<str:pk>/', views.markComplete, name="mark_complete"),
    path('mark_current/<str:pk>/', views.markCurrent, name="mark_current"),


    # URLs to find peers and tutors for classes
    path('find_peer/<str:pk1>/<str:pk2>', views.FindPeer.as_view()),
    path('find_tutor/<str:pk1>/<str:pk2>', views.FindTutor.as_view()),
]