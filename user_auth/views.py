import time
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import F
from django.http import JsonResponse
from django.db import transaction
from .models import Semesters, Programs, Batches, Subjects, Courses, CoursesBatches, Students, Results
from django.contrib.auth.models import User
import json


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['show_welcome'] = True
                return redirect("user_auth:dashboard")
            else:
                return render(request, "login.html", {'username': username})
        else:
            messages.error(request, "Invalid username or password.", extra_tags="login_only")
            return render(request, "login.html", {'username': username})

    return render(request, "login.html")


def custom_logout(request):
    logout(request)
    request.session.flush()
    return redirect("user_auth:login")


@login_required(login_url="user_auth:login")
def dashboard_view(request):
    
    context = {}
    show_welcome = request.session.pop('show_welcome', False)
    if show_welcome:
        context['show_welcome'] = True
    
    if request.user.groups.first().name == 'HOD':
        total_students = Students.objects.filter(auth_user__is_active=True).count()
        active_subjects = Subjects.objects.count()
        current_semester = Semesters.objects.order_by('-start_date').first()
        
        context.update({
            'total_students': total_students,
            'active_subjects': active_subjects,
            'current_semester': current_semester
        })
        
    if request.user.groups.first().name == 'Student':
        try:
            student = Students.objects.select_related('batches').get(auth_user_id=request.user.id)

            results = Results.objects.raw("""
                SELECT r.*, sb.name as subject_name, sb.total_credit 
                FROM results r
                JOIN courses c ON c.id = r.courses_id 
                JOIN subjects sb ON sb.id = c.subjects_id 
                WHERE r.students_id = %s                        
            """, [student.id])
            
            total_points = 0
            total_credits = 0
            grade_points = {
                'A+': 4.0, 'A': 4.0, 'A-': 3.7,
                'B+': 3.3, 'B': 3.0, 'B-': 2.7,
                'C+': 2.3, 'C': 2.0, 'C-': 1.7,
                'D+': 1.3, 'D': 1.0, 'F': 0.0
            }
            
            for result in results:
                grade_point = grade_points.get(result.grade, 0)
                credits = float(result.total_credit) if result.total_credit else 0
                total_points += grade_point * credits
                total_credits += credits
            
            current_gpa = round(total_points / total_credits, 2) if total_credits > 0 else 0
            
            context.update({
                'student': student,
                'current_gpa': current_gpa,
                'current_level': student.batches.current_level,  # Changed from batch_id to batches
                'results': results,
                'total_credits': total_credits
                
            })
            
        except Students.DoesNotExist:
            messages.error(request, "Student record not found.")
        except Exception as e:
            print(f"Error fetching dashboard data: {e}")
            messages.error(request, "Error loading dashboard data.")
            
    
    
    '''
    if request.user.groups.first().name == 'Student':
        try:
            student = Students.objects.get(auth_user_id=request.user.id)
            
            results = Results.objects.select_related(
                'courses',
                'courses__subjects'
            ).filter(
                students_id=student.id
            ).values(
                'courses__subjects__name',
                'grade'
            )
            
            context.update({
                'student': student,
                'results': results
            })
            
        except Students.DoesNotExist:
            messages.error(request, "Student record not found.")
    '''
    
            
        
    return render(request, "dashboard.html", context)



