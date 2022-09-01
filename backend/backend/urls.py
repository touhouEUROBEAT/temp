
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include("account.urls")),
    path('api/', include("api.urls")),
    path('connect/', include("connection.urls")),
    path('tutoring/', include("tutoring.urls")),
    path('review/', include("review.urls")),
    path('wait_time/', include("wait_time.urls")),
    path('karma/', include("karma.urls")),
    path('schedule/', include("schedule.urls"))
]
