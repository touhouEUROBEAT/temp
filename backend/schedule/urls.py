from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns=[
    path('get_schedule/', views.FetchScheduleView.as_view(), name='get_schedule'),
    path('update_schedule/', views.UpdateScheduleView.as_view(), name='update_schedule'),
    path('upload_schedule/', views.UploadScheduleView.as_view(), name='upload_schedule'),
    path('add_event/', views.AddEventView.as_view(), name='add_event'),
    path('delete_event/', views.DeleteEventView.as_view(), name='delete_event'),
]
