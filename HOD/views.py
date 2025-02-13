import time
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import F
from django.http import JsonResponse
from django.db import transaction
from datetime import datetime
from .models import *
import json

def semester_declaration(request):
    if request.method == "POST":
        try:
            start_date = request.POST.get("startDate")
            end_date = request.POST.get("endDate")

            # Validate if semester start date is valid
            if start_date >= end_date:
                messages.error(request, "Semester start date must be before the end date.")
                return redirect("HOD:semester_declaration")

            # Convert string dates to Python date objects
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

            # Fetch the most recent semester
            latest_semester = Semesters.objects.order_by("-end_date").first()

            #Validation: New semester should start after the latest semester ends
            if latest_semester and start_date <= latest_semester.end_date:
                messages.error(request, "New semester must start after the last semester's end date.")
                return redirect("HOD:semester_declaration")

            # Validation: Check if new semester overlaps with existing ones
            overlapping_semester = Semesters.objects.filter(start_date__lte=end_date, end_date__gte=start_date).exists()

            if overlapping_semester:
                messages.error(request, "The selected semester period overlaps with an existing semester.")
                return redirect("HOD:semester_declaration")

            # Transaction: Ensure data consistency
            with transaction.atomic():
                # Deactivate batches that reached level 8** (Graduated)
                Batches.objects.filter(is_active=True, current_level=8).update(current_level=-1, is_active=False)

                # Increment current level for active batches (<8)
                Batches.objects.filter(is_active=True, current_level__lt=8).update(current_level=F("current_level") + 1)

                # Mark the previous semester as completed
                Semesters.objects.filter(status=0).update(status=1)

                # Create new active semester
                semester = Semesters.objects.create(
                    start_date=start_date, end_date=end_date,status=0,
                )
        
            messages.success(request, "Semester declared successfully!")
            return redirect("HOD:semester_declaration")

        except Exception as e:
            messages.error(request, f"Error declaring semester: {str(e)}")

    # Get the most recent semester for display
    all_semesters = Semesters.objects.all().order_by("-start_date")

    context = {
        "all_semesters": all_semesters
    }

    return render(
        request, "HOD/semester_declaration.html", context
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
                
                batch_students = Students.objects.filter(batches_id=batch_id)
                batch = Batches.objects.get(id=batch_id)
                current_level = batch.current_level

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
                            batches_id=batch_id,
                            status=0
                        )

                        courses_students = []
                        for student in batch_students:
                            courses_students.append(
                                CoursesStudent(
                                    students=student,
                                    courses=course,
                                    level=current_level,
                                    attmp=1,
                                    marks=0
                                )
                            )
                        
                        CoursesStudent.objects.bulk_create(courses_students)

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