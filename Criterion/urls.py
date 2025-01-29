from django.urls import path
from . import views

app_name = 'Criterion'

urlpatterns = [
    path('add_criterion/', views.add_criterion, name='add_criterion'),
    path('get_batches/', views.get_batches, name='get_batches'),
    path('get_courses/', views.get_courses, name='get_courses'),
    path('get_next_ca_number/', views.get_next_ca_number, name='get_next_ca_number'),
    path('save_criteria/', views.save_criteria, name='save_criteria'),
    path('get_criteria/', views.get_criteria, name='get_criteria'),
]