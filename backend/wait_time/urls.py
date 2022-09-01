from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('data/', views.wait_time_data.as_view(), name='wait_time_data'),
]