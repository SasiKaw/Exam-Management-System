from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentRegistrationForm
from .models import *
from django.contrib.auth import logout as auth_logout
from django.http import JsonResponse
from django.db import transaction
import json


def student_registration(request):
    """
    Handles the student registration process.
    
    This view serves two purposes:
    1. For GET requests: Displays the registration form
    2. For POST requests: Processes the form submission, creates user and student records
    """
    batches = Batches.objects.all().order_by('name')
    
    # If the user is already logged in, redirect them to dashboard
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect('student:register')

    if request.method == 'POST':
        # Create a form instance with the submitted data
        form = StudentRegistrationForm(request.POST)
        
        if form.is_valid():
            try:
                # Save the user and create student record
                user = form.save()
                user.is_active = False
                user.save()
                
                # Add success message
                messages.success(
                    request, 
                    "Registration successful! Please log in with your credentials."
                )
                
                # Redirect to login page
                return redirect('user_auth:login')
                
            except Exception as e:
                # If something goes wrong during saving
                print(f"Registration Error: {str(e)}")
                messages.error(
                    request,
                    "An error occurred during registration. Please try again."
                )
        else:
            for field in form.errors:
                for error in form.errors[field]:
                    messages.error(request, f"{field}: {error}")
        
        
    else:
        # For GET requests, create an empty form
        form = StudentRegistrationForm()
    
    # Render the registration template with the form
    return render(request, 'student/registration.html', {'form': form, 'batches':batches})


def show_results(request):
    context = {}
    selected_semester = request.GET.get('semester')
    
    try:
        student = Students.objects.select_related('batches').get(auth_user_id=request.user.id)
        
        # Get all semesters for dropdown
        semesters = Semesters.objects.raw("""
            SELECT DISTINCT s.* 
            FROM semesters s
            JOIN courses c ON c.semesters_id = s.id
            JOIN results r ON r.courses_id = c.id
            WHERE r.students_id = %s
            ORDER BY s.start_date DESC
        """, [student.id])
        
        # Define grade points
        grade_points = {
            'A+': 4.0, 'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'D+': 1.3, 'D': 1.0, 'E': 0.0,
            'I': 0.0, 'T': 0.0, 'F': 0.0,
            'NC': 0.0, 'NE': 0.0, 'AC': 0.0,
            'AE': 0.0, 'AF': 0.0, 'NA': 0.0,
            'AA': 0.0, 'X': 0.0
        }

        # Base query to get results
        query = """
            SELECT r.*, 
                   sb.name as subject_name, 
                   sb.code as subject_code,
                   sb.total_credit,
                   s.start_date, s.end_date,
                   s.id as semester_id,
                   CONCAT('Semester ', s.id) as semester_name
            FROM results r
            JOIN courses c ON c.id = r.courses_id 
            JOIN subjects sb ON sb.id = c.subjects_id
            JOIN semesters s ON s.id = c.semesters_id
            WHERE r.students_id = %s
        """
        params = [student.id]
        
        if selected_semester:
            query += " AND s.id = %s"
            params.append(selected_semester)
            
        query += " ORDER BY s.start_date, sb.code"
        
        results = Results.objects.raw(query, params)
        
        # Process results semester by semester
        semester_stats = {}
        cumulative_stats = {
            'total_credits': 0,
            'total_gpv': 0,
            'courses_count': 0
        }
        
         # Initialize semester dictionary if not already created
        for result in results:
            semester_id = result.semester_id
            
            if semester_id not in semester_stats:
                semester_stats[semester_id] = {
                    'name': f"Semester {semester_id}",
                    'courses': [],
                    'credits': 0,
                    'gpv': 0,
                    'gpa': 0,
                    'cumulative_credits': 0,
                    'cumulative_gpv': 0,
                    'cumulative_gpa': 0
                }
            
            # Calculate course GPV
            credits = float(result.total_credit)
            grade_point = grade_points.get(result.grade, 0)
            course_gpv = credits * grade_point
            
            # Add course details
            course_detail = {
                'code': result.subject_code,
                'name': result.subject_name,
                'credits': credits,
                'grade': result.grade,
                'grade_point': grade_point,
                'gpv': course_gpv
            }
            
            semester_stats[semester_id]['courses'].append(course_detail)
            semester_stats[semester_id]['credits'] += credits
            semester_stats[semester_id]['gpv'] += course_gpv
            
            cumulative_stats['courses_count'] += 1
        
        # Calculate cumulative statistics
        running_credits = 0
        running_gpv = 0
        
        for semester_id in sorted(semester_stats.keys()):
            stats = semester_stats[semester_id]
            
            # Calculate semester GPA
            if stats['credits'] > 0:
                stats['gpa'] = round(stats['gpv'] / stats['credits'], 2)
            
            # Update running totals
            running_credits += stats['credits']
            running_gpv += stats['gpv']
            
            # Store cumulative statistics
            stats['cumulative_credits'] = running_credits
            stats['cumulative_gpv'] = running_gpv
            if running_credits > 0:
                stats['cumulative_gpa'] = round(running_gpv / running_credits, 2)
            
            # Update final stats
            cumulative_stats['total_credits'] = running_credits
            cumulative_stats['total_gpv'] = running_gpv
        
        # Calculate final CGPA
        cgpa = round(cumulative_stats['total_gpv'] / cumulative_stats['total_credits'], 2) \
               if cumulative_stats['total_credits'] > 0 else 0
        
        context.update({
            'student': student,
            'semesters': semesters,
            'selected_semester': selected_semester,
            'semester_stats': semester_stats,
            'cumulative_stats': cumulative_stats,
            'cgpa': cgpa
        })
        
    except Students.DoesNotExist:
        messages.error(request, "Student record not found.")
    except Exception as e:
        print(f"Error fetching results data: {e}")
        messages.error(request, "Error loading results data.")
    
    return render(request, 'student/results.html', context)


def show_repeat_courses(request):
    """
    Display repeat-eligible courses for the current student with their available repeat assessment options
    """
    context = {}
    
    try:
        # Get the current student record with related batch information
        student = Students.objects.select_related('batches').get(auth_user_id=request.user.id)
        
        # Define grades that make a student eligible for repeating
        failing_grades = ['C-', 'D+', 'D', 'E', 'NC', 'NE', 'AC', 'AE', 'AA', 'AF']
        
        # SQL query to fetch course details and repeat eligibility
        query = """
            SELECT 
                r.*,  -- All result fields
                sb.name as subject_name, 
                sb.code as subject_code,
                sb.total_credit as credits,
                sb.ca as ca_component,    -- Boolean indicating if course has CA component
                sb.fe as fe_component,    -- Boolean indicating if course has FE component
                c.id as course_id,
                
                -- Check if student already has a pending repeat application
                EXISTS(
                    SELECT 1 
                    FROM repeat_enrollment re 
                    WHERE re.courses_id = c.id 
                    AND re.students_id = %s
                ) as has_pending_application,
                
                -- Get the assessment components information
                (SELECT 
                    JSON_ARRAYAGG(
                        JSON_OBJECT(
                            'nature', cr.nature,
                            'type', cr.type,
                            'weights', cr.weights
                        )
                    )
                FROM criterias cr 
                WHERE cr.courses_id = c.id
                ) as assessment_details
                
            FROM results r
            JOIN courses c ON c.id = r.courses_id 
            JOIN subjects sb ON sb.id = c.subjects_id
            WHERE r.students_id = %s
            AND r.grade IN %s
            ORDER BY sb.code
        """
        
        # Execute the raw query with parameters
        repeat_courses = Results.objects.raw(
            query, 
            [student.id, student.id, tuple(failing_grades)]
        )
        
        # Process the results to determine eligible components
        processed_courses = []
        for course in repeat_courses:
            # Create a dictionary with course information
            course_dict = {
                'course_id': course.course_id,
                'subject_code': course.subject_code,
                'subject_name': course.subject_name,
                'credits': course.credits,
                'grade': course.grade,
                'has_pending_application': course.has_pending_application,
                'assessment_options': []  # List to store available assessment options
            }
          
            # Add CA option if course has CA component
            if course.ca_component > 0:  # Checking if there's a CA weightage
                course_dict['assessment_options'].append({
                    'value': 'CA',
                    'label': f'Continuous Assessment ({course.ca_component}%)'
                })
            
            # Add FE option if course has FE component
            if course.fe_component > 0:  # Checking if there's an FE weightage
                course_dict['assessment_options'].append({
                    'value': 'FE',
                    'label': f'Final Examination ({course.fe_component}%)'
                })
            
            processed_courses.append(course_dict)
        
        # Add processed courses to context
        context['repeat_courses'] = processed_courses
        
    except Students.DoesNotExist:
        messages.error(request, "Student record not found.")
    except Exception as e:
        print(f"Error fetching repeat courses: {e}")
        messages.error(request, "Error loading repeat courses data.")
    
    return render(request, 'student/repeat_courses.html', context)

@transaction.atomic
def apply_repeat(request):
    """
    Handle repeat course application submission
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    
    try:
        data = json.loads(request.body)
        course_id = data.get('course_id')
        assessment_type = data.get('assessment_type')
        
        if not all([course_id, assessment_type]):
            return JsonResponse({
                'status': 'error',
                'message': 'Missing required fields'
            })
        
        student = Students.objects.get(auth_user_id=request.user.id)
        
        # Check if application already exists
        existing_application = RepeatEnrollments.objects.filter(
            students=student,
            courses_id=course_id
        ).exists()
        
        if existing_application:
            return JsonResponse({
                'status': 'error',
                'message': 'Application already exists for this course'
            })
        
        # Create new repeat enrollment
        RepeatEnrollments.objects.create(
            students=student,
            courses_id=course_id,
            assessment_type=assessment_type,
            attemp_no=2  # You might want to calculate this based on previous attempts
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Application submitted successfully'
        })
        
    except Students.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Student record not found'
        })
    except Exception as e:
        print(f"Error processing repeat application: {e}")
        return JsonResponse({
            'status': 'error',
            'message': 'Failed to process application'
        })