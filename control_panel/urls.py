from django.urls import path, include
from . import views

app_name = 'control_panel'

urlpatterns = [
    path('', include('newsletters.urls')),
]