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
    path('ca_schedule/', views.ca_schedule_view, name='ca_schedule'),
    path('get_ca_criteria/', views.get_ca_criteria, name='get_ca_criteria'),
    path('save_ca_schedule/', views.save_ca_schedule, name='save_ca_schedule'),
    path('get_ca_events/', views.get_ca_events, name='get_ca_events'),
]