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
    
    try:
        student = Students.objects.select_related('batches').get(auth_user_id=request.user.id)

        results = Results.objects.raw("""
            SELECT r.*, sb.name as subject_name, sb.total_credit 
            FROM results r
            JOIN courses c ON c.id = r.courses_id 
            JOIN subjects sb ON sb.id = c.subjects_id 
            WHERE r.students_id = %s                        
        """, [student.id])
        
        context.update({
            'results': results,  
        })
        
    except Students.DoesNotExist:
        messages.error(request, "Student record not found.")
    except Exception as e:
        print(f"Error fetching dashboard data: {e}")
        messages.error(request, "Error loading dashboard data.")
    
    return render(request, 'student/results.html', context)