from django.urls import path
from . import views

app_name = 'connect'

urlpatterns = [
    path('match_sent/', views.MatchingSentView.as_view(), name='match_sent'),
    path('match_received/', views.MatchingReceivedView.as_view(), name='match_received'),
    path('generate_match/', views.GenerateMatchingView.as_view(), name='generate_match'),
    path('match_finalized/', views.MatchingFinalized.as_view(), name='match_finalized'),
    path('modify_pending/', views.ModifyPending.as_view(), name='modify_pending'),
    path('get_info/', views.GetInfo.as_view(), name='get_info'),
    path('get_info_test/', views.GetInfoTest.as_view(), name='get_info_test'),
    path('add_karma/', views.AddKarmaView.as_view(), name='add_karma'),
    path('get_pfp/', views.GetPFPView.as_view(), name='get_pfp'),
]
