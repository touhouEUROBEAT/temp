from django.urls import path
from . import views

urlpatterns=[
    
    path('<str:pk1>/<str:pk2>/', views.GetReviews.as_view(), name='get_reviews'),

]