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

    path('lecturer-assignment/', views.lecturer_assignment, name='lecturer_assignment'),
    path('assign-lecturer/<int:course_id>/', views.assign_lecturer, name='assign_lecturer'),
    path('remove-lecturer/<str:assignment_id>/', views.remove_lecturer, name='remove_lecturer'),
]
