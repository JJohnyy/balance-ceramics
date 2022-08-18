from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add/<item_slug>/', views.add_to_bag, name='add_to_bag'),
    path('update/<item_slug>/', views.update_bag, name='update_bag'),
    path('remove/<item_slug>/', views.remove_from_bag, name='remove_from_bag'),
]