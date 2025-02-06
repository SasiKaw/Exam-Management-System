import time
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import F
from django.http import JsonResponse
from django.db import transaction
from .models import Semesters, Programs, Batches, Subjects, Courses, CoursesBatches, Results
import json

def semester_declaration(request):
    if request.method == "POST":
        try:
            start_date = request.POST.get("startDate")
            end_date = request.POST.get("endDate")

            # Create new semester
            semester = Semesters.objects.create(
                start_date=start_date, end_date=end_date
            )

            active_batches = Batches.objects.filter(is_active=True)
            active_batches.update(current_level=F("current_level") + 1)

            messages.success(request, "Semester declared successfully!")
            return redirect("HOD:semester_declaration")

        except Exception as e:
            messages.error(request, f"Error declaring semester: {str(e)}")

    # Get the most recent semester for display
    all_semesters = Semesters.objects.all().order_by("-start_date")

    return render(
        request, "HOD/semester_declaration.html", {"all_semesters": all_semesters}
    )


def course_management(request):
    # Get semesters and programs for initial load
    semesters = Semesters.objects.order_by('-start_date').first()
    programs = Programs.objects.all()
    
    
    context = {
        "semesters": semesters,
        "programs": programs,
    }
    return render(request, "HOD/course_management.html", context)


def get_batches(request):
    program_id = request.GET.get("program_id")
    semester_id = request.GET.get("semester_id")
    batches = Batches.objects.filter(programs_id=program_id, is_active=1)
    data = list(batches.values("id", "name", "current_level"))
    
    batches = batches.exclude(
        id__in=CoursesBatches.objects.filter(
            courses__semesters_id=semester_id
        ).values('batches_id')
    )
    
    data = list(batches.values("id", "name", "current_level"))
    print(data)
    return JsonResponse({"batches": data})


def get_subjects(request):
    program_id = request.GET.get("program_id")
    subjects = Subjects.objects.filter(programs_id=program_id)
    data = list(subjects.values("id", "name", "level"))
    return JsonResponse({"subjects": data})


@transaction.atomic
def save_courses(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Received data:", data)  # Debug log
            
            if not data.get('assignments'):
                raise ValueError("No assignments provided")
                
            assignments = data['assignments']
            created_courses = []

            for assignment in assignments:
                print("Processing assignment:", assignment)  # Debug log
                
                semester_id = assignment.get('semester')
                batch_id = assignment.get('batch_id')
                subjects = assignment.get('subjects', [])

                if not semester_id:
                    raise ValueError("Missing semester ID")
                if not batch_id:
                    raise ValueError("Missing batch ID")
                if not subjects:
                    raise ValueError("No subjects provided")

                for subject in subjects:
                    subject_id = subject.get('id')
                    if not subject_id:
                        raise ValueError("Subject ID is missing")

                    try:
                        # Create course
                        course = Courses.objects.create(
                            semesters_id=semester_id,
                            subjects_id=subject_id
                        )
                        
                        # Create batch association
                        CoursesBatches.objects.create(
                            courses=course,
                            batches_id=batch_id
                        )
                        
                        created_courses.append(course.id)
                        
                    except Exception as e:
                        print(f"Error creating course: {str(e)}")  # Debug log
                        raise

            return JsonResponse({
                'status': 'success',
                'message': f'Successfully created {len(created_courses)} courses',
                'created_courses': created_courses
            })

        except ValueError as ve:
            print(f"Validation error: {str(ve)}")  # Debug log
            return JsonResponse({
                'status': 'error',
                'message': str(ve)
            }, status=400)
        except Exception as e:
            print(f"Unexpected error: {str(e)}")  # Debug log
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=400)


    
    data = list(batches.values("id", "name", "current_level"))
    return JsonResponse({"batches": data})

def validate_data(assignment):
    required_fields = ["semester", "batch_id", "subjects"]
    for field in required_fields:
        if field not in assignment:
            raise ValueError(f"Missing required field: {field}")

    if not assignment["subjects"]:
        raise ValueError("No subjects provided")

    for subject in assignment["subjects"]:
        if "id" not in subject:
            raise ValueError("Subject missing ID")