from django.urls import path
from . import views

urlpatterns = [
    path('', views.newsletter_signup, name='newsletter_signup'),
    path('newsletter_unsubscribe/', views.newsletter_unsubscribe, name='unsubscribe'),
   
]