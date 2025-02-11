from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentRegistrationForm
from .models import *
from django.contrib.auth import logout as auth_logout


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