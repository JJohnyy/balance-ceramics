from django.urls import path
from . import views


urlpatterns = [
    path('', views.newsletter_signup, name='newsletter_signup'),
    path('newsletter_unsubscribe/', views.newsletter_unsubscribe, name='news_unsubscribe'),
    path('contacts/', views.contact_view, name='contacts'),
    path('newsletter/', views.control_newsletter, name='control_newsletter')
]