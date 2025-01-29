from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    path('register/', views.student_registration, name='register'),
    path('results/', views.show_results, name='result'),
]