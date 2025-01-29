from django.urls import path
from . import views

app_name = 'Results'

urlpatterns = [
    path('boe/', views.result_view, name='get_result'),
    path('get-batches/', views.get_batches, name='get_batches'),
    path('get-courses/', views.get_courses, name='get_courses'),
    path('get-students/', views.get_students, name='get_students'),
    path('finalize/', views.finalize_dashboard, name='finalize_dashboard'),
    path('get-batch-courses/', views.get_batch_courses, name='get_batch_courses'),
    path('update-status/', views.update_course_status, name='update_status'),
    path('get-criteria/', views.get_criteria, name='get_criteria'),
    path('get-students-marks/', views.get_students_marks, name='get_students_marks'),
    path('save-criterion-marks/', views.save_criterion_marks, name='save_criterion_marks'),
    path('add-criterion-mark/', views.add_criterion_marks, name='add_criterion_marks'),
    path('get-grade-summary/', views.get_grade_summary, name='get_grade_summary'),
]