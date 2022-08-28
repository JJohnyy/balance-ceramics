from django.urls import path, include


app_name = 'control_panel'

urlpatterns = [
    path('', include('newsletters.urls')),
]
