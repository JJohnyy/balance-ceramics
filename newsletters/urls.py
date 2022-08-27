from django.urls import path
from . import views


urlpatterns = [
    path('', views.newsletter_signup, name='newsletter_signup'),
    path('newsletter_unsubscribe/', views.newsletter_unsubscribe, name='news_unsubscribe'),
    path('contacts/', views.contact_view, name='contacts'),
    path('newsletter/', views.control_newsletter, name='control_newsletter'),
    path('newsletter_list/', views.control_newsletter_list, name='control_newsletter_list'),
    path('newsletter_detail/<pk>/', views.control_newsletter_detail, name='control_newsletter_detail'),
    path('newsletter_edit/<pk>/', views.control_newsletter_edit, name='control_newsletter_edit'),
    path('newsletter_delete/<pk>/', views.control_newsletter_delete, name='control_newsletter_delete')
]
