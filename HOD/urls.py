from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'HOD'

urlpatterns = [
    path('semester-declaration/', views.semester_declaration, name='semester_declaration'),
    path('course-management/', views.course_management, name='course_management'),
    path('get-batches/', views.get_batches, name='get_batches'),
    path('get-subjects/', views.get_subjects, name='get_subjects'),
    path('save-courses/', views.save_courses, name='save_courses'),
]
