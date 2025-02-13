from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    path('register/', views.student_registration, name='register'),
    path('results/', views.show_results, name='result'),
    path('repeat-courses/', views.show_repeat_courses, name='repeat_courses'),
    path('apply-repeat/', views.apply_repeat, name='apply_repeat'),
]